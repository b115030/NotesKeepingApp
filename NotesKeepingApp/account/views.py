"""
Verifies email for authentication, password reset

* @Author: Gopinath

"""
import os
import jwt
import logging
import json
import redis
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import (generics, status, views)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializer import RegisterSerializer, SetNewPasswordSerializer, ResetPasswordEmailRequestSerializer, EmailVerificationSerializer, LoginSerializer
from .utils import Util
from notes.utils import token_dict
from NotesKeepingApp.settings import file_handler
from .utils import AccountError, NotFoundUserError
from notes.services import Cache
from notes.tasks import send_activation_mail

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

# rdb = redis.StrictRedis()
Cache = Cache()

class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class LoginAPIView(generics.GenericAPIView):
       
    serializer_class = LoginSerializer

    def post(self, request):
        """
        it verifies the credentials, if credentials were matched then returns data in json format, else throws exception

        Args:
            request : username, password

        Returns:
            Response (json): json data if credentials are matched
        """        
        # try:
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.data.get('email')
            # print(email)
            password = serializer.data.get('password')
            # print(password)
            user_login_details = User.objects.get(email = email)
            if user_login_details.is_active == False:
                raise AccountError("pleacse activate account")

                # if user_login_details.is_deleted == True:
                #     raise AccountError("Account has been deleted.")

                # user = authenticate(email=email, password=password)
                # print (user)
            # if user:
            if user_login_details.id is not None:
                user_id = user_login_details.id
                print(user_id)
            else:
                raise NotFoundUserError(user_login_details.id)
            return_token = jwt.encode({"user_id": user_id}, "secret", algorithm="HS256").decode('utf-8')
            print(return_token)
            Cache.set_cache("NOTE_FOR_UID_"+str(user_id), return_token)
            token_dict["Token"]=return_token
            result = {
                'message':"Log in suuccessful",
                'token': return_token,
            } 
            return Response(result, status.HTTP_200_OK) 
        except AccountError as e:
            logging.error(str(e))
            return Response("Error has occured!", status.HTTP_400_BAD_REQUEST) 

class UserLogoutView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        '''
        :param request: takes in a post request with no attributes
        :return: Returns a HTTP 200 after logging user out.
        '''

        token = request.headers.get('token')
        payload = jwt.decode(token, os.getenv('secret'), algorithm=os.getenv('algorithm'))
        user_id = payload.get('id')
        rdb.delete(user_id)
        smd = {
            'success': True,
            'message': 'Successfully Logged out',
            'data': []
        }

        return Response(data=smd, status=status.HTTP_200_OK)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        """
        create account for user by taking in user details

        Args:
            request ([type]): [description]

        Returns:
            Response (json): json data if credentials are matched
        """        
        message_dict = {
            'success': False,
            'message': "Successful Registration. Click The Link for verification!",
            'data': [],
        }
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            

            token = RefreshToken.for_user(user).access_token
            absolute_url = request.build_absolute_uri(reverse('email-verify')) + "?token=" + str(token)
            email_body = 'Hi ' + user.user_name + \
                        ', \n Use the link below to verify your email \n' + absolute_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}
            send_activation_mail.delay(data)
            logging.debug('validated data: {}'.format(serializer.data))
            user.is_active = False
            user.save()       

            context = {            
                'protocol': request.scheme,            
                'domain': request.META['HTTP_HOST'],      
            }

            send_activation_mail.delay(user.id, context) ## calling the task

            # return user
            message_dict['success']= True
            return Response(message_dict, status=status.HTTP_201_CREATED)
        except Exception as e:
            message_dict['message'] = "Error occured!"
            logger.error("error: %s ", str(e))
            return Response(message_dict, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        """verifies for credentials using wmail and then gives login access

        Args:
            request (HttpRequest): metadata of Notes 

        Returns:
            object : Rest framework Response object
        """       
        token = request.GET.get('token')

        message_dict = {
            'success': False,
            'message': "not verified",
        }
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()
                message_dict['success'] = True
                message_dict['message'] = 'Successfully activated'#change messgae
            return Response(message_dict, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            logger.error("error: %s ", str(e))
            message_dict['success'] = False
            message_dict['message'] = 'Activation Expired'
            return Response(message_dict, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            logger.error("error: %s ", str(e))
            message_dict['success'] = False
            message_dict['message'] = 'Invalid token'
            return Response(message_dict, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        """[summary]

        Args:
            request ([type]): [description]

        Returns:
            [type]: [description]
        """        

        message_dict = {
            'success': False,
            'message': "not verified",
        }

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            redirect_url = reverse('password-reset-complete')
            absolute_url = request.build_absolute_uri(reverse('password-reset-confirm'))
            email_body = 'Hello, \n Your token number is : ' + token + ' \n your uidb64 code is ' + uidb64 + ' \n Use link below to reset your password  \n' + \
                         absolute_url + "?redirect_url=" + redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            send_activation_mail.delay(data)
            message_dict['success']=True
            message_dict['message']='We have sent you a link to reset your password'
            return Response(message_dict, status=status.HTTP_200_OK)
        else:
            message_dict['message']="Email id you have entered doesn't exist"
            return Response(message_dict, status=status.HTTP_200_OK)



class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request):

        """[summary]

        Returns:
            [type]: [description]
        """        
        redirect_url = request.GET.get('redirect_url')
        if redirect_url and len(redirect_url) > 3:
            return CustomRedirect(
                redirect_url + '?token_valid=True&message=Credentials Valid')
        else:
            return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        """[summary]

        Args:
            request ([type]): [description]

        Returns:
            [type]: [description]
        """        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)