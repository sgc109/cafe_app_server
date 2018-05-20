from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import *
from django.db import IntegrityError
from .models import Profile
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
    query_set = Profile.objects.all().filter(id=id)
    cnt = query_set.count()
    if cnt > 0:
        if cnt > 1:
            return HttpResponse('multiple accounts!')
        profile = query_set[0]
        serializer = ProfileSerializer(profile)
        return HttpResponse('login success!')
    else:
        return HttpResponse('invalid user')
