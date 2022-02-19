from django.contrib import admin
from .models import User, Profile
# Register your models here.

class UserAdmin(admin.ModelAdmin):

    list_display = ['username', 'first_name', 'last_name', 'email' , 'is_premium', 'is_active']

admin.site.register(User, UserAdmin)

class ProfileAdmin(admin.ModelAdmin):

    list_display = ['photo', 'user',]

admin.site.register(Profile, ProfileAdmin)