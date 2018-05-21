from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import *
from django.db import IntegrityError
from .models import Profile
from .serializer import ProfileSerializer
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def add_user(request):
    id = request.GET.get('id', '')
    pw = request.GET.get('pw', '')
    new_user = User(username=id, password=pw)
    try:
        new_user.save()
        profile = Profile(user=new_user, name='test_name', profile_image='', comment='')
        profile.save()
    except IntegrityError as e:
        return JsonResponse({}, status=400)
        #return HttpResponse(e.__cause__)

    return JsonResponse({}, status=200)

def remove_user(request):
    id = request.GET.get('id', '')
    pw = request.GET.get('pw', '')
    query_set = User.objects.all().filter(username=id, password=pw)
    cnt = query_set.count()
    if cnt > 0:
        if cnt > 1:
            return JsonResponse({}, status=400)
        query_set.delete()
        return JsonResponse({}, status=200)
    else:
        return JsonResponse({}, status=400)

def login(request):
    id = request.GET.get('id', '')
    pw = request.GET.get('pw', '')
    if User.objects.all().filter(username=id, password=pw).count() == 0:
        return JsonResponse({}, status=400)

    query_set = User.objects.all().filter(username=id)
    cnt = query_set.count()
    if cnt > 0:
        if cnt > 1:
            return JsonResponse({}, status=400)
        user = query_set[0]
        profile = Profile.objects.all().filter(user=user)[0]
        profile_serializer = ProfileSerializer(profile, context={'request': request})
        return JsonResponse(profile_serializer.data, status=200)
    return JsonResponse({}, status=400)

@csrf_exempt
def change_profile_image(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    query_set = User.objects.all().filter(username=id, password=pw)
    cnt = query_set.count()
    if cnt > 0:
        if cnt > 1:
            return JsonResponse({}, status=400)
        user = query_set[0]
        profile = Profile.objects.all().filter(user=user)[0]
        profile.profile_image = request.FILES['file']
        profile.save()
        return JsonResponse({}, status=200)
    else:
        return JsonResponse({}, status=400)
