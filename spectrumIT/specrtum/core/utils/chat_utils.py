from core.models.base_models import User
from core.models.slider_models import UserLikedStatusStorage, Swipe
from core.models.chat_models import ChatRoom
from core.utils.db_utils import create_slug_field_between_two_users
from exeptions.core_exeptions import ErrorDuringCreationUserLikedStatusBetweenTwoUsers, ErrorDuringStartingChatBetweenTwoUsers
from django.db.utils import IntegrityError


def has_liked_status_between_two_users(user1: User, user2: User) -> bool:
    users_search_slug = create_slug_field_between_two_users(user1, user2)

    try:
        liked_status_between_two_users = UserLikedStatusStorage.objects.get(users_search_slug=users_search_slug)
    except Exception:
        liked_status_between_two_users = None

    if liked_status_between_two_users:
        return True
    else:
        return False

def create_user_liked_status_between_two_users_or_raise_error(cur_user: User, target_user: User) -> UserLikedStatusStorage | ErrorDuringCreationUserLikedStatusBetweenTwoUsers:
    try:
        liked_status_between_two_users = UserLikedStatusStorage.objects.create(
            initiator_user=cur_user,
            target_user=target_user,
        )

        liked_status_between_two_users.save()
        return liked_status_between_two_users
    except ErrorDuringCreationUserLikedStatusBetweenTwoUsers as err:
        raise err()
    
def check_possibility_to_start_new_chat_between_two_users(cur_user: User, target_user: User) -> bool:
    users_search_slug = create_slug_field_between_two_users(cur_user, target_user)
    liked_status_between_two_users = UserLikedStatusStorage.objects.get(users_search_slug=users_search_slug)

    if liked_status_between_two_users.target_user == cur_user:    # e.g cur_user received a message about sympathy
        return True
    else:
        return False

def start_chat_between_two_users_or_raise_error(user1: User, user2: User, is_approved_start_chat: bool) -> ChatRoom | ErrorDuringStartingChatBetweenTwoUsers:
    if is_approved_start_chat:
        start_chat_between_two_users(user1, user2)
    else:
        raise ErrorDuringStartingChatBetweenTwoUsers()  
    
def start_chat_between_two_users(user1: User, user2: User) -> ChatRoom | ErrorDuringStartingChatBetweenTwoUsers:
    try:
        chat_room = ChatRoom.objects.create(
            name=create_slug_field_between_two_users(user1, user2),
        )
        
        chat_room.participants.set([user1, user2])
        chat_room.save()

        return chat_room
    except ErrorDuringStartingChatBetweenTwoUsers as err:
        raise err()
    
def record_swipe(swiper, swiped_on, liked):
    try:
        Swipe.objects.create(swiper=swiper, swiped_on=swiped_on, liked=liked)
    except IntegrityError as err:
        # log action
        ...
