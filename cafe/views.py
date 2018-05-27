from django.http import *
from .models import *
from .serializer import *
from django.contrib.auth.models import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db import IntegrityError
from django.core import serializers
from django.forms import ModelForm
from pyfcm import FCMNotification
import json

def error_response():
    return JsonResponse({},status=400)

def success_response():
    return JsonResponse({},status=200)

@csrf_exempt
def login(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    if User.objects.all().filter(username=id, password=pw).count() == 0:
        return error_response()

    query_set = User.objects.all().filter(username=id)
    cnt = query_set.count()

    if cnt > 0:
        if cnt > 1:
            return error_response()
        user = query_set[0]
        profile = Profile.objects.all().filter(user=user)[0]
        profile_serializer = ProfileSerializer(profile)
        return JsonResponse(profile_serializer.data, status=200)
    else:
        return error_response()


@csrf_exempt
def add_user(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    name = request.POST.get('name', '')
    fcm_token = request.POST.get('fcm_token', '')
    if not id or not pw:
        return error_response()
    new_user = User(username=id, password=pw)
    try:
        new_user.save()
        profile = Profile(user=new_user, name=name, profile_image='default_profile_image.png', comment='', fcm_token=fcm_token)
        profile.save()
    except IntegrityError as e:
        return error_response()

    return success_response()

@csrf_exempt
def remove_user(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    query_set = User.objects.all().filter(username=id, password=pw)
    user = query_set[0]
    profile = Profile.objects.all().filter(user=user)
    try:
        query_set.delete()
        return success_response()

    except:
        return error_response()

@csrf_exempt
def remove_user_by_id(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    uid = int(request.POST.get('uid'))
    user = User.objects.all().filter(username=id, password=pw)[0]
    profile = Profile.objects.all().filter(user=user)[0]
    if profile.type == 0:
        return JsonResponse({}, status=401)
    query_set = User.objects.all().filter(id=uid)
    query_set.delete()
    return success_response()

@csrf_exempt
def edit_user(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    name = request.POST.get('name', '')
    image = request.FILES.get('image', '')
    comment = request.POST.get('comment', '')
    user = User.objects.all().filter(username=id, password=pw)[0]
    profile = Profile.objects.all().filter(user=user)[0]
    if name:
        profile.name = name
    if image:
        profile.profile_image = image
    if comment:
        profile.comment = comment
    profile.save()
    serial = ProfileSerializer(profile)
    return JsonResponse(serial.data, status=200)

@csrf_exempt
def edit_user_by_id(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    uid = int(request.POST.get('uid'))
    name = request.POST.get('name', '')
    image = request.FILES.get('image', '')
    comment = request.POST.get('comment', '')
    admin_user = User.objects.all().filter(username=id, password=pw)[0]
    admin_profile = Profile.objects.all().filter(user=admin_user)[0]
    if admin_profile.type == 0:
        return JsonResponse({}, status=401)
    user = User.objects.all().filter(id=uid)[0]
    profile = Profile.objects.all().filter(user=user)[0]

    if name:
        profile.name = name
    if image:
        profile.profile_image = image
    if comment:
        profile.comment = comment
    profile.save()
    serial = ProfileSerializer(profile)
    return JsonResponse(serial.data, status=200)

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
    except:
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

@csrf_exempt
def upload_post(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    title = request.POST.get('title', '')
    text = request.POST.get('text', '')
    try:
        user = User.objects.all().filter(username=id, password=pw)[0]
        profile = Profile.objects.all().filter(user=user)[0]
        post = Post(profile=profile, image=request.FILES['image'], title=title, text=text)
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
        profile = Profile.objects.all().filter(user=user)
        post = Post.objects.all().filter(id=post_id, profile=profile)
        post.delete()
        return success_response()
    except:
        return error_response()

@csrf_exempt
def get_posts(request):

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
    post_query_set = Post.objects.all().order_by('-id')
    if last_post_id != -1:
        post_query_set = post_query_set.filter(id__lt=last_post_id)
    posts = post_query_set[:cnt_post]
    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, status=200, safe=False)

@csrf_exempt
def get_profiles(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    user = User.objects.all().filter(username=id, password=pw)[0]
    profile = Profile.objects.all().filter(user=user)[0]
    if profile.type == 0:
        return JsonResponse({}, status=401)
    profiles = Profile.objects.all()
    serial = ProfileSerializer(profiles, many=True)
    return JsonResponse(serial.data, status=200, safe=False)

@csrf_exempt
def create_category(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    user = User.objects.all().filter(username=id, password=pw)[0]
    profile = Profile.objects.all().filter(user=user)[0]
    if profile.type == 0:
        return JsonResponse({}, status=401)
    name = request.POST.get('name')
    category = Category(name=name)
    category.save()
    serial = CategorySerializer(category)
    return JsonResponse(serial.data, status=200)

@csrf_exempt
def delete_category(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    user = User.objects.all().filter(username=id, password=pw)[0]
    profile = Profile.objects.all().filter(user=user)[0]
    if profile.type == 0:
        return JsonResponse({}, status=401)
    category_id = request.POST.get('category_id', '')
    query_set = Category.objects.all().filter(id=category_id)
    query_set.delete()
    return success_response()

def get_categories(request):
    categories = Category.objects.all()
    serial = CategorySerializer(categories, many=True)
    return JsonResponse(serial.data, status=200, safe=False)

@csrf_exempt
def create_menu(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    user = User.objects.all().filter(username=id, password=pw)[0]
    profile = Profile.objects.all().filter(user=user)[0]
    if profile.type == 0:
        return JsonResponse({}, status=401)

    category_id = request.POST.get('category_id', '')
    type = Category.objects.all().filter(id=category_id)[0]
    name = request.POST.get('name')
    price = int(request.POST.get('price'))
    image = request.FILES['image']
    if not image:
        image = 'default_coffee.png'
    taking_time = int(request.POST.get('taking_time'))
    menu = Menu(type=type, name=name, price=price, image=image, taking_time=taking_time)
    menu.save()
    serial = MenuSerializer(menu)

    return JsonResponse(serial.data, status=200)

@csrf_exempt
def delete_menu(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    user = User.objects.all().filter(username=id, password=pw)[0]
    profile = Profile.objects.all().filter(user=user)[0]
    if profile.type == 0:
        return JsonResponse({}, status=401)
    menu_id = request.POST.get('menu_id', '')
    if menu_id:
        menu_id = int(menu_id)
    query_set = Menu.objects.all().filter(id=menu_id)[0]
    query_set.delete()
    return success_response()

@csrf_exempt
def edit_menu(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    category_id  = request.POST.get('category_id', '')
    price = int(request.POST.get('price', ''))
    name = request.POST.get('name', '')
    image = request.FILES.get('image', '')
    taking_time = int(request.POST.get('taking_time', ''))
    menu_id = request.POST.get('menu_id', '')
    user = User.objects.all().filter(username=id, password=pw)[0]
    profile = Profile.objects.all().filter(user=user)[0]
    menu = Menu.objects.all().filter(id=menu_id)[0]
    type = Category.objects.all().filter(id=category_id)[0]

    if profile.type == 0:
        return JsonResponse({}, status=401)

    menu.type = type
    menu.price = price
    menu.name = name
    if image:
        menu.image = image
    menu.taking_time = taking_time
    menu.save()
    serial = MenuSerializer(menu)
    return JsonResponse(serial.data, status=200)

def get_menus(request):
    menus = Menu.objects.all()
    serial = MenuSerializer(menus, many=True)
    return JsonResponse(serial.data, status=200, safe=False)

@csrf_exempt
def create_order(request):
    data = json.loads( request.body.decode('utf-8'))
    id = data.get('id', '')
    pw = data.get('pw', '')
    user = User.objects.all().filter(username=id, password=pw)[0]
    profile = Profile.objects.all().filter(user=user)[0]

    comment = data.get('comment')
    item_list = data.get('item_list')
    price_sum = 0
    time_sum = 0

    for item in item_list:
        menu_id = item.get('menu_id')
        cnt = int(item.get('cnt'))
        menu = Menu.objects.all().filter(id=menu_id)[0]
        price = int(menu.price)
        price_sum += price * cnt
        time_sum += int(menu.taking_time) * cnt

    order = Order(profile=profile, comment=comment, taking_time=time_sum, price=price_sum)
    order.save()

    profile.point += int(price_sum * 0.01)
    profile.save()

    for item in item_list:
        menu_id = item.get('menu_id')
        menu = Menu.objects.get(id=menu_id)
        cnt = int(item.get('cnt'))
        order_item = OrderItem(order=order, menu=menu, cnt=cnt)
        order_item.save()

    return JsonResponse({'test': price_sum}, status=200)

@csrf_exempt
def get_orders(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    state = int(request.POST.get('state', 2))
    year = request.POST.get('year', '')
    month = request.POST.get('month', '')

    user = User.objects.all().filter(username=id, password=pw)[0]
    profile = Profile.objects.all().filter(user=user)[0]
    query_set = Order.objects.all()
    if state != 2:
        query_set = query_set.filter(state=state)
    if profile.type == 0:
        query_set = query_set.filter(profile=profile)
    if year:
        query_set = query_set.filter(date__year=int(year))
    if month:
        query_set = query_set.filter(date__month=int(month))
    query_set = query_set.order_by('state', 'date')
    serial = OrderSerializer(query_set, many=True)
    return JsonResponse(serial.data, status=200, safe=False)

@csrf_exempt
def get_order_by_id(request):
    id = request.POST.get('id')
    pw = request.POST.get('pw')
    order_id = request.POST.get('order_id')
    user = User.objects.all().filter(username=id, password=pw)[0]
    profile = Profile.objects.all().filter(user=user)[0]
    order = Order.objects.all().filter(id=order_id)[0]
    if profile.type == 0 and profile.user.id != order.profile.user.id:
        return error_response()
    items = OrderItem.objects.all().filter(order=order)
    serial = OrderItemSerializer(items, many=True)
    return JsonResponse(serial.data, safe=False)

@csrf_exempt
def change_order_state(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    order_id  = request.POST.get('order_id', '')
    order = Order.objects.all().filter(id=order_id)[0]
    user = User.objects.all().filter(username=id, password=pw)[0]
    profile = Profile.objects.all().filter(user=user)[0]

    if profile.type == 0:
        return JsonResponse({}, status=401)
    order.state = 1
    order.save()

    api_key = 'AAAA3VWD52A:APA91bG9O59Tk9931Ty1WIz2uh6ZdVtSdVhJsKYPPaZubQyxxdPFcspmVlB6VkeyHHwASTiFQEuWWh45aYo_GGMk6cLRR7_FTxcaecSnEMf-EwAHKb_-8sO5xNu2i2PZkneRq0Ys2Hm1'
    push_service = FCMNotification(api_key=api_key)
    registration_id = profile.fcm_token
    message_title = 'CAFE MIDAS'
    message_body = '주문하신 제품이 준비되었습니다. 빨리 찾아가세요!'
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

    return success_response()

def get_waiting_time(request):
    query_set = Order.objects.all().filter(state=0)
    ret = 0
    for order in query_set:
        ret += order.taking_time

    return JsonResponse({'waiting_time': ret}, status=200)

@csrf_exempt
def test_fcm(request):
    id = request.POST.get('id', '')
    pw = request.POST.get('pw', '')
    user = User.objects.all().filter(username=id, password=pw)[0]
    profile = Profile.objects.all().filter(user=user)[0]

    api_key = 'AAAA3VWD52A:APA91bG9O59Tk9931Ty1WIz2uh6ZdVtSdVhJsKYPPaZubQyxxdPFcspmVlB6VkeyHHwASTiFQEuWWh45aYo_GGMk6cLRR7_FTxcaecSnEMf-EwAHKb_-8sO5xNu2i2PZkneRq0Ys2Hm1'
    push_service = FCMNotification(api_key=api_key)
    registration_id = profile.fcm_token
    message_title = 'title'
    message_body = 'body'
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
    return success_response()

def get_waiting_order(request):
    return JsonResponse({'waiting_cnt': Order.objects.all().filter(state=0).count()}, status=200)
