from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Menu)
admin.site.register(WaitingTime)
