from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import *
from .serializer import *
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
        return success_response()
    except:
        return error_response()

@csrf_exempt
def delete_post(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    post_id = request.POST.get('post_id', 0)
    try:
        user = User.objects.all().filter(username=id, password=pw)[0]
        post = Post.objects.all().filter(id=post_id, user=user)
        post.delete()
        return success_response()
    except:
        return error_response()

@csrf_exempt
def get_posts(request):
    try:
        last_post_id = request.GET.get('last_post_id', -1)
        if not last_post_id:
            last_post_id = -1
        else:
            last_post_id = int(last_post_id)
        cnt_post = request.GET.get('cnt_post', 10)
        if not cnt_post:
            cnt_post = 10
        else:
            cnt_post = int(cnt_post)
        post_query_set = Post.objects.all().order_by('-created_date')
        if last_post_id != -1:
            post_query_set = post_query_set.filter(id__gt=last_post_id)
        posts = post_query_set[:cnt_post]
        serializer = PostSerializer(posts, many=True, context={"request": request})
        return JsonResponse(serializer.data, status=200, safe=False)
    except:
        return error_response()
