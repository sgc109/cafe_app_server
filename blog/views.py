from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import *

def upload_post(request):
    if request.method == 'GET':
        return JsonResponse({}, status=400)

    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    user_query_set = User.objects.all().filter(username=id, password=pw)
    if user_query_set.count() == 0:
        return JsonResponse({}, status=400)
    user = user_query_set[0]
    post = Post(user=user, image=request.FILES, title='test_title', text='test_text')
    post.save()

    return JsonResponse({}, status=200)

def delete_post(request):
    return JsonResponse({}, status=400)
