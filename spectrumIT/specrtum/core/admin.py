from django.contrib import admin
from core.models.base_models import User
from core.models.slider_models import UserMessageStorage, Swipe
from core.models.chat_models import ChatRoom, Message

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'age']

@admin.register(UserMessageStorage)
class UserMessageStorageAdmin(admin.ModelAdmin):
    list_display = ('target_user', 'message', 'created_at')

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    # list_display = ('target_user', 'message', 'created_at')
    ...
    
@admin.register(Swipe)
class SwipeAdmin(admin.ModelAdmin):
    # list_display = ('target_user', 'message', 'created_at')
    ...

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    # list_display = ('target_user', 'message', 'created_at')
    ...