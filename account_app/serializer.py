from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
#    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('name', 'profile_image', 'comment')
'''
    def get_photo_url(self, car):
        request = self.context.get('request')
        photo_url = car.photo.url
        return request.build_absolute_uri(photo_url)
'''
