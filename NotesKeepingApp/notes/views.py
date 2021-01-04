import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from .serializers import NotesSerializer
from .models import Note
from rest_framework.views import APIView
from .decorators import login_view_decorator
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.Cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from django.views.decorators.Cache import Cache_page
from .utils import NotesError
from .services import Cache
from django.db.models import Q


Cache_TTL = getattr(settings, 'Cache_TTL', DEFAULT_TIMEOUT)

User = get_user_model()
SEARCH_DATA =[]
@method_decorator(login_view_decorator, name='dispatch')
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
                return Response(message_dict, status.HTTP_201_CREATED)
            message_dict['message'] = "title has to be of max length 50"
            logging.debug('{}'.format(message_dict))
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message_dict['message'] = str(e)
            logging.debug('{}'.format(message_dict))
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """takes key as input, if exists in db, return the data 

        Returns:
            message_dict: success or failure message along with status
        """         
        message_dict = {
            'message': 'error has occured',
            'status': False,
            'data': [],
        }
        try:
            item = Note.objects.get(pk=kwargs.get('pk'))
            serializer = NotesSerializer(item)
            if serializer.data.get('is_deleted') == False:
                message_dict['message']= "Successful"
                message_dict['data'] = serializer.data
                message_dict['status'] = True
                return Response(message_dict, status.HTTP_200_OK)
            message_dict['message'] = "The data has been deleted"
        except Note.DoesNotExist :
            message_dict['message']="No such note found"
            logging.debug('{}'.format(message_dict))
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message_dict['message'] = str(e)
            logging.debug('{}'.format(message_dict))
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
            message_dict['message'] = "No such label found"#
            message_dict['status'] = False
            logging.debug('{}'.format(message_dict))
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message_dict['message'] = str(e)
            logging.debug('{}'.format(message_dict))
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
            note.soft_delete()
            message_dict['message'] = 'label deleted'
            message_dict['status'] = True
            logging.debug('{}'.format(message_dict))
            return Response(message_dict, status.HTTP_202_ACCEPTED)

        except Exception as e:
            message_dict['message'] = str(e)
            logging.debug('{}'.format(message_dict))
            return Response(message_dict, status.HTTP_404_NOT_FOUND)

@method_decorator(login_view_decorator, name='dispatch')
class AllNotesAPI(APIView):
    serializer_class = NotesSerializer

    def get(self, request, *args, **kwargs):
        """takes key as input, if exists in db, return the data 

        Returns:
            message_dict: success or failure message along with status
        """         
        message_dict = {
            'message': 'error has occured',
            'status': False,
            'data': [],
        }
        try:
            item = Note.objects.all()
            serializer = NotesSerializer(item)
            if serializer.data.get('is_deleted') == False:
                message_dict['message']= "Successful"
                message_dict['data'] = serializer.data
                message_dict['status'] = True
                return Response(message_dict, status.HTTP_200_OK)
            message_dict['message'] = "The data has been deleted"
        except Note.DoesNotExist :
            message_dict['message']="No such note found"
            logging.debug('{}'.format(message_dict))
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            message_dict['message'] = str(e)
            logging.debug('{}'.format(message_dict))
            return Response(message_dict, status.HTTP_400_BAD_REQUEST)


@method_decorator(login_view_decorator, name='dispatch')
class NoteArchive(APIView):
    def get(self, request, *args, **kwargs):
        logged_user = kwargs.get('user')
        try:
            if not Cache.get_cache(str(logged_user.id)):#"ARCHIVED_NOTES"
                notes = Note.objects.filter(is_archived = True)

                if not notes:
                    raise NotesError("No notes archived")

                serilaze = NotesSerializer(notes, many=True)
                Cache.set_cache(str(logged_user.id), serilaze)#"ARCHIVED_NOTES"
            else:
                serilaze = Cache.get_cache(str(logged_user.id))
            response = {'message':"Successful", 'status':True, 'data':serilaze.data}
            return Response(response, status=status.HTTP_200_OK)
        except NotesError as e:
            logging.warning(e)
            response = {'message':str(e), 'status':False, 'data':serilaze.data}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist as e:
            logging.warning(e)
            response = {'message':str(e), 'status':False, 'data':serilaze.data}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {'message':str(e), 'status':False, 'data':serilaze.data}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@method_decorator(login_view_decorator, name='dispatch')
class NoteTrash(APIView):
    def get(self, request, *args, **kwargs):
        
        logged_user = kwargs.get('user')
        try:
            if not Cache.get_cache(str(logged_user.id)):#"TRASHED_NOTES"
                notes = Note.objects.filter(trash = True)

                if not notes:
                    raise NotesError("No trashed notes")

                serilaze = NotesSerializer(notes, many=True)
                Cache.set_cache(str(logged_user.id), serilaze)#"TRASHED_NOTES"
            else:
                serilaze = Cache.get_cache(str(logged_user.id))#"TRASHED_NOTES"
                response = {'message':"successful", 'status':False, 'data':serilaze.data}
            return Response(response, status=status.HTTP_200_OK)
        except NotesError as e:
            logging.warning(e)
            response = {'message':str(e), 'status':False, 'data':serilaze.data}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist as e:
            logging.warning(e)
            response = {'message':str(e), 'status':False, 'data':serilaze.data}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.error(e)
            response = {'message':str(e), 'status':False, 'data':serilaze.data}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(login_view_decorator, name='dispatch')
class NotePinned(APIView):
    def get(self, request, *args, **kwargs):
        
        logged_user = kwargs.get('user')
        try:
            if not Cache.get_cache(str(logged_user.id)):
                notes = Note.objects.filter(is_pinned = True)

                if not notes:
                    raise NotesError("No pinned notes")

                serilaze = NotesSerializer(notes, many=True)
                Cache.set_cache(str(logged_user.id), serilaze)#"PINNED_NOTES"+
            else:
                serilaze = Cache.get_cache(+str(logged_user.id))#"PINNED_NOTES"
                response = {'message':"successful", 'status':False, 'data':serilaze.data}
            return Response(response, status=status.HTTP_200_OK)
        except NotesError as e:
            logging.warning(e)
            response = {'message':str(e), 'status':False, 'data':serilaze.data}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        except Note.DoesNotExist as e:
            logging.warning(e)
            response = {'message':str(e), 'status':False, 'data':serilaze.data}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {'message':str(e), 'status':False, 'data':serilaze.data}
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


