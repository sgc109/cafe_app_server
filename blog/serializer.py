from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post
from account_app.serializer import *

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'image', 'text', 'created_date', 'user', 'id')
