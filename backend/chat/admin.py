from django.contrib import admin
from .models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'phone' )
    search_fields = ('username', 'email', 'phone')

class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('slug',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'user', 'created_at')

admin.site.register(User, UserAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
