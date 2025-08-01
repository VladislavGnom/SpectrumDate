from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from core.utils.utils import get_chats_of_user, get_cur_user, get_user_by_id
from core.utils.chat_utils import (has_liked_status_between_two_users, create_user_liked_status_between_two_users_or_raise_error,
                                   check_possibility_to_start_new_chat_between_two_users, start_chat_between_two_users_or_raise_error)
from exeptions.core_exeptions import ErrorDuringGettingUsers


@login_required
def chat_user(request: HttpRequest, chat_user: int):

    context = {
        'title': 'Spectrum Date'
    }

    return render(request, 'core/chat_user.html', context=context)

@login_required
def chats(request: HttpRequest):
    cur_user = get_cur_user(request)
    chats_of_user = get_chats_of_user(cur_user)

    context = {
        'title': 'Spectrum Date',
        'chats': chats_of_user,
    }

    return render(request, 'core/chat_user.html', context=context)

def create_new_chat_with_validation_or_user_liked_status_between_two_users(request: HttpRequest):
    data_about_users = request.GET
    cur_user_id = data_about_users.get('cur_user')
    target_user_id = data_about_users.get('target_user')

    try:
        cur_user = get_user_by_id(cur_user_id)
        target_user = get_user_by_id(target_user_id)
    except ErrorDuringGettingUsers as err:
        raise err()
 
    if not has_liked_status_between_two_users(cur_user, target_user):
        create_user_liked_status_between_two_users_or_raise_error(cur_user, target_user)
    else:
        is_approved_start_chat = check_possibility_to_start_new_chat_between_two_users(cur_user, target_user)     
        start_chat_between_two_users_or_raise_error(cur_user, target_user, is_approved_start_chat)

    return JsonResponse({'status': 200})
