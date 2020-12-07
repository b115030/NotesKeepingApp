from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
# from .models import Account

#Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    '''
    RegisterSerializer handles user registration
    '''
    class Meta:
        model = User
        fields = ('id','username','password','first_name', 'last_name')
        extra_kwargs = {
            'password':{'write_only': True},
        }     
        def create(self, validated_data):
            user = User.objects.create_user(validated_data['username'], password = validated_data['password'], first_name=validated_data['first_name'],  last_name=validated_data['last_name'])
            return user
        
# User serializer
class UserSerializer(serializers.ModelSerializer):
    '''
    UserSerializer is used to retrive particular values of the users.
    '''
    class Meta:
        model = User
        fields = '__all__'

# class AccountDetailSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Account
#         fields = ('id','first_name', 'last_name' ,'username', 'email' , 'password','date_joined','last_login')