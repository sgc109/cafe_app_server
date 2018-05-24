from django.contrib.auth.models import User
from rest_framework import serializers
from account_app.serializer import *
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('name', 'photo_url', 'comment')

    def get_photo_url(self, profile):
        request = self.context.get('request')
        photo_url = profile.profile_image.url
        return request.build_absolute_uri(photo_url)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

class ProfileImageSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('photo_url', )

    def get_photo_url(self, profile):
        request = self.context.get('request')
        photo_url = profile.profile_image.url
        return request.build_absolute_uri(photo_url)
