from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import *
from django.views.decorators.csrf import csrf_exempt

def error_response():
    return JsonResponse({},status=400)

def success_response():
    return JsonResponse({},status=200)

@csrf_exempt
def upload_post(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    title = request.POST.get('title', '')
    text = request.POST.get('text', '')
    try:
        user = User.objects.all().filter(username=id, password=pw)[0]
        post = Post(user=user, image=request.FILES['image'], title=title, text=text)
        post.save()
        return success_response() # 포스트 목록 보내주는코드로 변경?
    except:
        return error_response()

@csrf_exempt
def delete_post(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    post_id = request.POST.get('post_id', '')
    try:
        user = User.objects.all().filter(username=id, password=pw)[0]
        post = Post.objects.all().filter(id=post_id, user=user)
        post.delete()
        return success_response()
    except:
        return error_response()
