from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post
from account_app.serializer import *

class PostSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    profile = ProfileSerializer()
    class Meta:
        model = Post
        fields = ('title', 'photo_url', 'text', 'created_date', 'id', 'profile')

    def get_photo_url(self, post):
        request = self.context.get('request')
        photo_url = post.image.url
        return request.build_absolute_uri(photo_url)
