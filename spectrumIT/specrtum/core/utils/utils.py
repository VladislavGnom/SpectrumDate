from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from core.models.chat_models import ChatRoom
from core.models.base_models import User

def get_chats_of_user(user: User) -> list[ChatRoom]:
    chat_rooms = user.chat_rooms.all()

    return list(chat_rooms)

def get_cur_user(request: HttpRequest) -> User:
    return request.user

def get_user_by_id(user_id: int) -> User:
    return User.objects.get(pk=user_id)
