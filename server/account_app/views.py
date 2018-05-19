from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import * 
from django.db import IntegrityError

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
    profile = Profile.objects.all().filter(id=id)
    return HttpResponse('')
