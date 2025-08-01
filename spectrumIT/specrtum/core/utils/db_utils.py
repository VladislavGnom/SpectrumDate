from django.conf import settings

User = settings.AUTH_USER_MODEL

def create_slug_field_between_two_users(user1: User, user2: User):
    return "-".join(map(
        str,
        sorted([user1, user2], key=lambda user: user.pk)
    ))
