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
            message_dict['message'] = "invalid data"
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message_dict['message'] = str(e)
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        
        message_dict = {
            'message': 'error has occured',
            'status': False
        }
        try:
            item = Note.objects.get(pk=kwargs.get('pk'))
            serializer = NotesSerializer(item)
            message_dict['message'] = serializer.data
            message_dict['status'] = True
            return Response(message_dict, status.HTTP_200_OK)
        except Exception as e:
            message_dict['message'] = str(e)
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
       
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
            message_dict['message'] = "enter valid details"
            message_dict['status'] = False
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message_dict['message'] = str(e)
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        
        message_dict = {
            'message': 'error has been occurred',
            'status': False
        }
        try:
            note = Note.objects.get(id=kwargs.get('pk'))
            note.delete()
            message_dict['message'] = 'Note deleted'
            message_dict['status'] = True
            return Response(message_dict, status.HTTP_202_ACCEPTED)

        except Exception as e:
            message_dict['message'] = str(e)
            return Response(message_dict, status.HTTP_404_NOT_FOUND)