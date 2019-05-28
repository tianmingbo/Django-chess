from django.contrib import admin
from .models import *


# Register your models here.
class UserInfoConfig(admin.ModelAdmin):
    list_display = ["username", "email", "score"]


admin.site.register(UserInfo, UserInfoConfig)
