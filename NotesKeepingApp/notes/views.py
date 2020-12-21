from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from .serializers import NotesSerializer
from .models import Note
from rest_framework.views import APIView

User = get_user_model()


class NotesAPI(APIView):
    serializer_class = NotesSerializer

    def post(self, request):
        """takes in notes data as inpu if valid, stores the data in database

        Args:
            request

        Returns:
            message_dict: success or failure message along with status
        """        
        message_dict = {
            'message': 'error occurred!',
            'status': False
        }
        try:

            serializer = NotesSerializer(data=request.data)
            if request.data['title'] is None or request.data['description'] is None:
                message_dict['message'] = "Enter title and description"
                return Response(message_dict, status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                serializer.save()
                message_dict['message'] = "Note added"
                message_dict['status'] = True
                return Response(message_dict)
            message_dict['message'] = "title has to be of max length 50"
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message_dict['message'] = str(e)
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """takes key as input, if exists in db, return the data 

        Returns:
            message_dict: success or failure message along with status
        """         
        message_dict = {
            'message': 'error has occured',
            'status': False
        }
        try:
            item = Note.objects.get(pk=kwargs.get('pk'))
            serializer = NotesSerializer(item)
            if serializer.data.get('is_deleted') == False:
                message_dict['message'] = serializer.data
                message_dict['status'] = True
                return Response(message_dict, status.HTTP_200_OK)
            message_dict['message'] = "The data has been deleted"
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
        message_dict = {
            'message': 'error has occured',
            'status': False
        }
        try:

            item = Note.objects.get(pk=kwargs.get('pk'))
            data = request.data
            serializer = NotesSerializer(item, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                message_dict['message'] = "Note updated"
                message_dict['status'] = True
                return Response(message_dict, status.HTTP_201_CREATED)
            message_dict['message'] = "title has to be of max length 50"
            message_dict['status'] = False
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message_dict['message'] = str(e)
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):

        """takes in key as input, if data exists, deletes the data from db

        Returns:
            message_dict: success or failure message along with status
        """       
        message_dict = {
            'message': 'error has been occured',
            'status': False
        }
        try:
            note = Note.objects.get(id=kwargs.get('pk'))
            note.delete()
            message_dict['message'] = 'label deleted'
            message_dict['status'] = True
            return Response(message_dict, status.HTTP_202_ACCEPTED)

        except Exception as e:
            message_dict['message'] = str(e)
            return Response(message_dict, status.HTTP_404_NOT_FOUND)