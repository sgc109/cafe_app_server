from django.contrib.auth.models import User
from rest_framework import serializers
from cafe.serializer import *
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    uid = serializers.ReadOnlyField(source='alias_user')

    class Meta:
        model = Profile
        exclude = ('user', )

# class ProfileImageSerializer(serializers.ModelSerializer):
#     photo_url = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Profile
#         fields = ('photo_url', )
#
# class ProfileNameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ('name', )
#
# class ProfileCommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ('comment', )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        exclude = ()

class OrderItemSerializer(serializers.ModelSerializer):
    menu = MenuSerializer()
    class Meta:
        model = OrderItem
        exclude = ()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', )

class OrderSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = Order
        exclude = ()
