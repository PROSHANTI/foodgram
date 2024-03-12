from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

from users.models import Follow

admin.site.register(Follow)
admin.site.register(User, UserAdmin)
