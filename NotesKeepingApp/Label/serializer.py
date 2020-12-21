from rest_framework import serializers
from .models import Label


class LabelSerializer(serializers.ModelSerializer):
    """[summary]

    Args:
        serializers ([type]): [description]
    """    

    class Meta:
        model = Label
        fields = ('user', 'label_name')