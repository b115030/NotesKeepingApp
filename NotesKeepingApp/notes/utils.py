import enum
from django.http.response import JsonResponse
from rest_framework import status
from .services import Cache
import jwt
import logging
from account.models import User

Cache = Cache()
token_dict = {"Token":""}

class ExceptionType(enum.Enum):
    UnknownError = "Error has occurred"
    NotesDoesnotExist = "No such notes Exist"
    LabelDoesnotExist = "No such labels exist"
    NoteNotFoundError = "No such notes found"

class NotesError(Exception):
    """[summary]
        Custom exception.
    Args:
        Exception ([Class]): [Exception]
    """
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message

def manage_response(**kwargs):
    """[summary]

    Returns:
        [type]: [description]
    """    
    response = {}
    response['message']=kwargs.get('message')
    response['status']=kwargs.get('status')

    if kwargs.get('data'):
        response['data']=kwargs.get('data')

    return response



def login_view_decorator(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            request_token = request.META['HTTP_TOKEN']
        
        # except InvalidSignatureError:
        #     return JsonResponse(data={"message": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        # if token_dict.get("Token") == request_token:
            decodedPayload = jwt.decode(request_token, "secret", algorithm="HS256")#//TODO: secret key and algorithm
            print(str(decodedPayload)+'hello!!')
            if Cache.get_cache(decodedPayload.get('user_id')) is not None:
                print("Hello,World!! Cahce is getting")
                print(decodedPayload['user_id'])
                # request.user = User.objects.get(id = decodedPayload.get('id') )
                kwargs['userid'] = decodedPayload['user_id']
                print(kwargs['userid'])

                
                return view_func(request, *args, **kwargs)
            #//TODO: empty token error handling
            #//TODO: unmatched id error handling
            # return JsonResponse(data={"message": "UnSuccessful"}, status=status.HTTP_400_BAD_REQUEST)
            # if user_id == id:
        except jwt.ExpiredSignature as e:
            logging.exception('exception occurred = {}, status code = {}'.format(str(e), status.HTTP_403_FORBIDDEN))
            return JsonResponse(data={"message": "Expired Signature"}, status=status.HTTP_403_FORBIDDEN)
        except jwt.exceptions.DecodeError as e:
            logging.exception('exception occurred = {}, status code = {}'.format(str(e), status.HTTP_403_FORBIDDEN))
            return JsonResponse(data={"message": "Invalid Token"}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logging.exception('exception occurred = {}, status code = {}'.format(str(e), status.HTTP_403_FORBIDDEN))
            return JsonResponse(data={"message": "Exception occurred!!!!"}, status=status.HTTP_403_FORBIDDEN)

    return wrapper