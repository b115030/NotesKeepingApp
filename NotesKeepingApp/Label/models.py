from django.db import models

# Create your models here.
from account.models import User


# Label model
class Label(models.Model):
    """Label model

    Inherits:
        models.Model

    Returns:
        Charfield: label_name
    """    
    label_name = models.CharField(max_length=50)  # for label name
    created_time = models.DateTimeField(auto_now_add=True, null=True)  # created time of labels
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='+')  # user details

    def __str__(self):
        return self.label_name