from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializer import LabelSerializer
from .models import Label
from rest_framework.views import APIView

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
    
        message_dict = {
            'message': 'error occurred',
            'status': False
        }
        try:

            serializer = LabelSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                message_dict['message'] = "Label has been added!"
                message_dict['status'] = True
                return Response(message_dict)
            message_dict['message'] = "label name should be of max length 50"
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message_dict['message'] = str(e)
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)

    def get(self, *args, **kwargs):
        """takes key as input, if exists in db, return the data 

        Returns:
            message_dict: success or failure message along with status
        """        
        message_dict = {
            'message': 'Some error occured',
            'status': False
        }
        try:
            item = Label.objects.get(pk=kwargs.get('pk'))
            serializer = LabelSerializer(item)
            message_dict['message'] = serializer.data
            message_dict['status'] = True
            return Response(message_dict, status.HTTP_200_OK)
        except Exception as e:
            message_dict['message'] = str(e)
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        """takes in label, if valid then updates the data in database

        Args:
            request 

        Returns:
            message_dict: success or failure message along with status
        """        
        #comments
        message_dict = {
            'message': 'error has occurred',
            'status': False
        }
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
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message_dict['message'] = str(e)#don't pass to user
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)

    def delete(self, *args, **kwargs):
        """takes in key as input, if data exists, deletes the data from db

        Returns:
            message_dict: success or failure message along with status
        """        
        message_dict = {
            'message': 'error has been occured',
            'status': False
        }
        try:
            note = Label.objects.get(id=kwargs.get('pk'))
            note.delete()
            message_dict['message'] = 'label deleted'
            message_dict['status'] = True
            return Response(message_dict, status.HTTP_202_ACCEPTED)

        except Exception as e:
            message_dict['message'] = str(e)
            return Response(message_dict, status.HTTP_404_NOT_FOUND)