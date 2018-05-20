from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import *
from django.db import IntegrityError
from .models import Profile
from .serializer import ProfileSerializer
from django.core import serializers
from django.http import JsonResponse

def add_user(request):
    id = request.GET.get('id', '')
    pw = request.GET.get('pw', '')
    new_user = User(username=id, password=pw)
    try:
        new_user.save()
    except IntegrityError as e:
        return HttpResponse(e.__cause__)

    return HttpResponse('sign up success!')

def remove_user(request):
    id = request.GET.get('id', '')
    pw = request.GET.get('pw', '')
    query_set = User.objects.all().filter(username=id, password=pw)
    cnt = query_set.count()
    if cnt > 0:
        if cnt > 1:
            return HttpResponse('multiple accounts!')
        query_set.delete()
        return HttpResponse('remove success!')
    else:
        return HttpResponse('invalid id or password!')

def login(request):
    id = request.GET.get('id', '')
    pw = request.GET.get('pw', '')
    if User.objects.all().filter(username=id, password=pw).count() == 0:
        return HttpResponse('invalid id or password!')

    query_set = User.objects.all().filter(username=id)
    cnt = query_set.count()
    if cnt > 0:
        if cnt > 1:
            return HttpResponse('multiple accounts!')
        user = query_set[0]
        profile = Profile.objects.all().filter(user=user)[0]
        profile_serializer = ProfileSerializer(profile, context={'request': request})
        return JsonResponse(profile_serializer.data)
        #data = serializers.serialize('json', Profile.objects.all().filter(user=user), fields=('name', 'profile_image', 'comment'))
        #return HttpResponse('login success!')
    return HttpResponse('invalid user')
