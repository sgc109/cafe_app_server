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
    url(r'^login/', cafe.views.login, name = 'login'),
    url(r'^change_profile_image/', cafe.views.change_profile_image, name = 'change_profile_image'),
    url(r'^change_profile_name/', cafe.views.change_profile_name, name = 'change_profile_name'),
    url(r'^change_profile_comment/', cafe.views.change_profile_comment, name = 'change_profile_comment'),
    # url(r'^upload_post/', blog.views.upload_post, name = 'upload_post'),
    # url(r'^delete_post/', blog.views.delete_post, name = 'delete_post'),
    # url(r'^get_posts/', blog.views.get_posts, name = 'get_posts'),
    # url(r'^api-token-auth/', obtain_jwt_token),
    # url(r'^api-token-refresh/', refresh_jwt_token),
    # url(r'^api-token-verify/', verify_jwt_token),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
