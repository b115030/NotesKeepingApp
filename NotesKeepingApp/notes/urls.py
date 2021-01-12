from django.conf.urls.static import static
from .views import NoteSearch, NotePinned, NoteArchive, NotesAPI, AllNotesAPI, NoteTrash
from django.conf import settings
from django.urls.conf import path

app_name = "notes"

urlpatterns = [
    path('pinned', NotePinned.as_view(), name="Pinned"),
    path('archive', NoteArchive.as_view(), name="Archive"),
    path('trash', NoteTrash.as_view(), name="Trash"),
    path('search/<str:search_for>', NoteSearch.as_view(), name="NoteSearch"),
    path('create-note/', NotesAPI.as_view(), name="AddNote"),
    path('note/<int:pk>', NotesAPI.as_view(), name='UpdateNote'),
    path('note/', NotesAPI.as_view(), name='GetAllNote'),

]