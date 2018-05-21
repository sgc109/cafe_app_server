from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import *

def error_response():
    return JsonResponse({},status=400)

def success_response():
    return JsonResponse({},status=200)

def upload_post(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    user_query_set = User.objects.all().filter(username=id, password=pw)
    if user_query_set.count() == 0:
        return error_response()
    user = user_query_set[0]
    post = Post(user=user, image=request.FILES['image'], title='test_title', text='test_text')
    try:
        post.save()
        return success_response() # 포스트 목록 보내주는코드로 변경?
    except:
        return error_response()

def delete_post(request):
    return success_response()
