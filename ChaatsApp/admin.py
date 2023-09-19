from django.contrib import admin
from .models import CustomUser, UserProfile, Message
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'profile_picture', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('sender__username', 'receiver__username', 'content')
