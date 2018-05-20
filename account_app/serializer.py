from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('name', 'profile_image')
