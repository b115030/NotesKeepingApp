from django.db import models
from django.db import models
from django.conf import settings
from colorful.fields import RGBColorField
from colorfield.fields import ColorField
from account.models import User
#     label = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="label", blank=True)

class Note(models.Model):
    title = models.CharField(max_length=150, default=None) 
    description = models.TextField() 
    created_time = models.DateTimeField(auto_now_add=True, null=True)  
    is_archived = models.BooleanField(default=False)  
    is_deleted = models.BooleanField(default=False) 
    color = ColorField(default='#00F0FF') 
    image = models.ImageField(upload_to='note_images/', default=None, null=True)  
    trash = models.BooleanField(default=False)  
    is_pinned = models.BooleanField(default=False)  
    label = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="label", blank=True)
    collaborate = models.ManyToManyField(User, null=True, blank=True, related_name='collaborated_user') 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', null=True, blank=True)  
    archive_time = models.DateTimeField(blank=True, null=True) 
    trash_time = models.DateTimeField(blank=True, null=True) 
    reminder_date = models.DateTimeField(blank=True, null=True)  



    def __str__(self):
        return self.title + " " + self.description

    def soft_delete(self):
        self.is_deleted = True
        self.save()  
