from django.urls import path
from django.contrib.auth import views as auth_views
from core.views import register, base_views, chat_views, notifications_views, search_views, slider_views


urlpatterns = [
    path('', base_views.main_page_view, name='main'),
    path('chats', chat_views.chats, name='chats'),
    path('chat/<int:chat_user>', chat_views.chat_user, name='chat_user'),
    path('search', search_views.search_page_view, name='search'),
    path('load-another-user', slider_views.load_another_user, name='load_another_user'),
    path('slider', slider_views.slider, name='slider'),
    path('slider/<int:user_id>', slider_views.slider_by_id, name='slider_by_id'),
    path('record-swipe', slider_views.record_swipe_view, name='record_swipe'),

    path('send-message/<int:user_id>', notifications_views.create_user_notification, name='send_message'),
    path('my-notifications', notifications_views.user_notifications, name='notifications'),
    path('create-chat-if-possible', chat_views.create_new_chat_with_validation_or_user_liked_status_between_two_users, name='create_chat_if_possible'),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', register.register, name='register'),
]
