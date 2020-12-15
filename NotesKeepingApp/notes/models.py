from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Label(models.Model):
    name = models.CharField("name of label", max_length=254)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='label_user', default="admin")

    def __str__(self):
        return self.name
   

    def __repr__(self):
        return "Label({!r},{!r})".format(self.user, self.name)

    class Meta:
    
        verbose_name = 'label'
        verbose_name_plural = 'labels'


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=500, blank=True, )
    description = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to="media")
    is_archive = models.BooleanField(verbose_name="is_archived", default=False)
    is_trashed = models.BooleanField(verbose_name="delete_note", default=False)
    label = models.ManyToManyField(Label, related_name="label", blank=True)
    collaborators = models.ManyToManyField(User, related_name='collaborators', blank=True)
    is_copied = models.BooleanField(verbose_name="make a copy", default=False)
    checkbox = models.BooleanField(verbose_name="check box", default=False)
    is_pinned = models.BooleanField(verbose_name="is pinned", default=False)
    reminder = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return "Note({!r},{!r},{!r})".format(self.user, self.title, self.description)

    class Meta:
    
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

