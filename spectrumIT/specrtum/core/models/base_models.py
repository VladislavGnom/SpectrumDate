from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = 'male', 'Мужской'
        FEMALE = 'female', 'Женский'
        ANOTHER = 'another', 'Другой'

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        default=GenderChoices.MALE
    )
    # location = models.PointField(geography=True, blank=True, null=True)
    interests = models.ManyToManyField('Interest', blank=True)
    is_verified = models.BooleanField(default=False)
    
    def str(self):
        return self.username

    # def save(self, *args, **kwargs):
    #     self.birthdate = timezone.make_aware(self.birthdate)
    #     today = timezone.make_aware(timezone.now())
    #     age = today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
    #     self.age = age
    #     super().save(*args, **kwargs)
