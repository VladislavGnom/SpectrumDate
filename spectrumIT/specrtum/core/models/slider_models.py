from django.db import models
from core.utils.db_utils import create_slug_field_between_two_users


class UserMessageStorage(models.Model):
    target_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_messages')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.target_user
    

class UserLikedStatusStorage(models.Model):
    initiator_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='chat_initiator_user')
    target_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='chat_target_user')
    users_search_slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ['initiator_user', 'target_user']

    def str(self):
        return self.target_user
    
    @staticmethod
    def is_approved(self):
        ...

    def save(self, *args, **kwargs):
        self.users_search_slug = create_slug_field_between_two_users(self.initiator_user, self.target_user)
        super().save(*args, **kwargs)


class Swipe(models.Model):
    swiper = models.ForeignKey('User', on_delete=models.CASCADE, related_name='swipes_made')
    swiped_on = models.ForeignKey('User', on_delete=models.CASCADE, related_name='swipes_received')
    liked = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('swiper', 'swiped_on')

    def __str__(self):
        return f"{self.swiper} {self.swiped_on} ({'like' if self.liked else 'dislike'})"


class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name