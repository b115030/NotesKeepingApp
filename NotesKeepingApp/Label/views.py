import logging
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializer import LabelSerializer
from .models import Label
from rest_framework.views import APIView
from .utils import response_dictionary
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

logging.basicConfig(filename='logs/NotesKeepingApp.log', level=logging.DEBUG,
                    format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')

# Create your views here.

class Labels(APIView):
    serializer_class = LabelSerializer

    def post(self, request):
        """label data as inpu if valid, stores the data in database

        Args:
            request

        Returns:
            message_dict: success or failure message along with status
        """        
    
        # message_dict = {
        #     'message': 'error occurred',
        #     'status': False,
        #     'data':[],
        # }
        # log_dict = message_dict
        try:

            serializer = LabelSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                result_dict = response_dictionary("Label has been added!", True, serializer.data)
                # message_dict['message'] = "Label has been added!"
                # message_dict['status'] = True
                # message_dict['data'] = serializer.data
                logging.debug('{}'.format(result_dict))
                return Response(result_dict, status.HTTP_200_OK)
            result_dict = response_dictionary("label name should be of max length 50", False, serializer.data)
            # message_dict['message'] = 
            logging.debug('{}'.format(result_dict))
            return Response(result_dict, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            result_dict = response_dictionary("Internal Error Occurred", False, str(e))
            logging.debug('{}'.format(result_dict))
            return Response(result_dict, status.HTTP_400_BAD_REQUEST)

    def get(self, *args, **kwargs):
        """takes key as input, if exists in db, return the data 

        Returns:
            message_dict: success or failure message along with status
        """        
        # message_dict = {
        #     'message': 'Some error occured',
        #     'status': False,
        #     'data' : [],
        # }
        # log_dict = message_dict
        try:
            item = Label.objects.get(pk=kwargs.get('pk'))
            serializer = LabelSerializer(item)
            result_dict = response_dictionary("Successful", True, serializer.data)
            # message_dict['data'] = serializer.data
            # message_dict['message'] = "Successful"
            # message_dict['status'] = True
            logging.debug('{}'.format(result_dict))
            return Response(result_dict, status.HTTP_200_OK)
        except Label.DoesNotExist as e:
            result_dict = response_dictionary("The Label doest not exist", False, str(e))
            # message_dict['message'] = 
            # log_dict['message'] = str(e)
            # logging.debug('{}'.format(log_dict))
            return Response(result_dict, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result_dict = response_dictionary("Internal error has occured", False, str(e))
            # message_dict['message'] = 
            # log_dict['message'] = str(e)
            logging.debug('{}'.format(result_dict))
            return Response(result_dict, status.HTTP_400_BAD_REQUEST)
        

    def put(self, request, *args, **kwargs):
        """takes in label, if valid then updates the data in database

        Args:
            request 

        Returns:
            message_dict: success or failure message along with status
        """        
        message_dict = {
            'message': 'error has occurred',
            'status': False
        }
        log_dict = message_dict
        try:

            item = Label.objects.get(pk=kwargs.get('pk'))#modeldoesnotexist eror handling
            data = request.data
            serializer = LabelSerializer(item, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                message_dict['message'] = "label updated"
                message_dict['status'] = True
                return Response(message_dict, status.HTTP_201_CREATED)
            message_dict['message'] = "label name should be of max length 50"
            message_dict['status'] = False
            logging.debug('{}'.format(message_dict))
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)
        except Label.ModelDoesnotExist as e:
            result_dict = response_dictionary("The Label doest not exist", False, str(e))
            # message_dict['message'] = 
            # log_dict['message'] = str(e)
            # logging.debug('{}'.format(log_dict))
            return Response(result_dict, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            result_dict = response_dictionary("Internal error has occured", False, str(e))
            # message_dict['message'] = 
            # log_dict['message'] = str(e)
            logging.debug('{}'.format(result_dict))
            return Response(result_dict, status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        """takes in key as input, if data exists, deletes the data from db

        Returns:
            message_dict: success or failure message along with status
        """        
        message_dict = {
            'message': 'error has been occured',
            'status': False
        }
        log_dict = message_dict
        try:
            note = Label.objects.get(id=kwargs.get('pk'))
            note.soft_delete()
            message_dict['message'] = 'label deleted'
            message_dict['status'] = True
            logging.debug('{}'.format(message_dict))
            return Response(message_dict, status.HTTP_202_ACCEPTED)

        except Exception as e:
            result_dict = response_dictionary("Internal error has occured", False, str(e))
            # message_dict['message'] = 
            # log_dict['message'] = str(e)
            logging.debug('{}'.format(result_dict))
            return Response(result_dict, status.HTTP_400_BAD_REQUEST)