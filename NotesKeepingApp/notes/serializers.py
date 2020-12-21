from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note

class NotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ('user', 'title', 'description', 'is_archived',
                  'color', 'image', 'is_pinned',
                  'is_deleted', 'label', 'collaborate', 'archive_time', 'trash_time', 'reminder_date')