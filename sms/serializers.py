from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields="__all__"


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']

            
        
