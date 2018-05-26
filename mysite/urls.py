from django.conf.urls import url, include
from django.contrib import admin
import cafe.views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^add_user/', cafe.views.add_user, name = 'add_user'),
    url(r'^remove_user/', cafe.views.remove_user, name = 'remove_user'),
    url(r'^edit_user/', cafe.views.edit_user, name = 'edit_user'),
    url(r'^edit_user_by_id/', cafe.views.edit_user_by_id, name = 'edit_user_by_id'),
    url(r'^remove_user_by_id/', cafe.views.remove_user_by_id, name = 'remove_user_by_id'),
    url(r'^login/', cafe.views.login, name = 'login'),
    url(r'^change_profile_image/', cafe.views.change_profile_image, name = 'change_profile_image'),
    url(r'^change_profile_name/', cafe.views.change_profile_name, name = 'change_profile_name'),
    url(r'^change_profile_comment/', cafe.views.change_profile_comment, name = 'change_profile_comment'),
    url(r'^get_profiles/', cafe.views.get_profiles, name = 'get_profiles'),
    url(r'^create_category/', cafe.views.create_category, name = 'create_category'),
    url(r'^get_categories/', cafe.views.get_categories, name = 'get_categories'),
    url(r'^delete_category/', cafe.views.delete_category, name = 'delete_category'),
    url(r'^create_menu/', cafe.views.create_menu, name = 'create_menu'),
    url(r'^delete_menu/', cafe.views.delete_menu, name = 'delete_menu'),
    url(r'^edit_menu/', cafe.views.edit_menu, name = 'edit_menu'),
    url(r'^get_menus/', cafe.views.get_menus, name = 'get_menus'),
    url(r'^create_order/', cafe.views.create_order, name = 'create_order'),
    url(r'^get_waiting_time/', cafe.views.get_waiting_time, name = 'get_waiting_time'),
    url(r'^get_orders/', cafe.views.get_orders, name = 'get_orders'),
    url(r'^get_order_by_id/', cafe.views.get_order_by_id, name = 'get_order_by_id'),
    # url(r'^upload_post/', blog.views.upload_post, name = 'upload_post'),
    # url(r'^delete_post/', blog.views.delete_post, name = 'delete_post'),
    # url(r'^get_posts/', blog.views.get_posts, name = 'get_posts'),
    # url(r'^api-token-auth/', obtain_jwt_token),
    # url(r'^api-token-refresh/', refresh_jwt_token),
    # url(r'^api-token-verify/', verify_jwt_token),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
