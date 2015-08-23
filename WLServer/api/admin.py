#coding:utf-8
from django.contrib import admin
from api.models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('uid', 'name', 'sex', 'birthday', 'city', 'pwd', 'access_token')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'type', 'to_user')

class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'pics', 'from_user')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'status', 'from_user')

class NewFriendAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'status', 'to_user')

admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Newfriend, NewFriendAdmin)
admin.site.register(Comment)

