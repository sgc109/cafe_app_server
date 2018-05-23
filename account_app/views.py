from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import *
from django.db import IntegrityError
from .models import Profile
from .serializer import *
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def error_response():
    return JsonResponse({},status=400)

def success_response():
    return JsonResponse({},status=200)

def add_user(request):
    id = request.GET.get('id', '')
    pw = request.GET.get('pw', '')
    new_user = User(username=id, password=pw)
    try:
        new_user.save()
        profile = Profile(user=new_user, name='', profile_image='', comment='')
        profile.save()
    except IntegrityError as e:
        return error_response()
        #return HttpResponse(e.__cause__)

    return success_response()

def remove_user(request):
    id = request.GET.get('id', '')
    pw = request.GET.get('pw', '')
    query_set = User.objects.all().filter(username=id, password=pw)
    cnt = query_set.count()
    try:
        if cnt > 0:
            if cnt > 1:
                return error_response()
            query_set.delete()
            return success_response()
        else:
            return error_response()
    except:
        return error_response()

def login(request):
    id = request.GET.get('id', '')
    pw = request.GET.get('pw', '')
    if User.objects.all().filter(username=id, password=pw).count() == 0:
        return error_response()

    query_set = User.objects.all().filter(username=id)
    cnt = query_set.count()
    try:
        if cnt > 0:
            if cnt > 1:
                return error_response()
            user = query_set[0]
            profile = Profile.objects.all().filter(user=user)[0]
            profile_serializer = ProfileSerializer(profile)
            return JsonResponse(profile_serializer.data, status=200)
        else:
            return error_response()
    except:
        return error_response()

@csrf_exempt
def change_profile_image(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    query_set = User.objects.all().filter(username=id, password=pw)
    cnt = query_set.count()
    try:
        if cnt > 0:
            if cnt > 1:
                error_response()
            user = query_set[0]
            profile = Profile.objects.all().filter(user=user)[0]
            prv_photo = profile.profile_image
            if prv_photo:
                prv_photo.delete()
            profile.profile_image = request.FILES['photo']
            profile.save()
            serializer = ProfileImageSerializer(profile)
            return JsonResponse(serializer.data, status=200)
        else:
            return error_response()
    except Exception as e:
        return error_response()

@csrf_exempt
def change_profile_name(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    query_set = User.objects.all().filter(username=id, password=pw)
    cnt = query_set.count()
    try:
        if cnt > 0:
            if cnt > 1:
                error_response()
            user = query_set[0]
            profile = Profile.objects.all().filter(user=user)[0]
            profile.name = request.POST.get('name', '')
            profile.save()
            serializer = ProfileNameSerializer(profile)
            return JsonResponse(serializer.data, status=200)
        else:
            return error_response()
    except Exception as e:
        return error_response()

@csrf_exempt
def change_profile_comment(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    query_set = User.objects.all().filter(username=id, password=pw)
    cnt = query_set.count()
    try:
        if cnt > 0:
            if cnt > 1:
                error_response()
            user = query_set[0]
            profile = Profile.objects.all().filter(user=user)[0]
            profile.comment = request.POST.get('comment', '')
            profile.save()
            serializer = ProfileCommentSerializer(profile)
            return JsonResponse(serializer.data, status=200)
        else:
            return error_response()
    except Exception as e:
        return error_response()
