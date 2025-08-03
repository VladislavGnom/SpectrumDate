from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.dateparse import parse_date
from django.forms import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = 'male', 'Мужской'
        FEMALE = 'female', 'Женский'
        ANOTHER = 'another', 'Другой'

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.jpg')
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
    birthdate = models.DateField(blank=True)
    
    def str(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.birthdate and not self.age:
            self._set_age()
        super().save(*args, **kwargs)

    def _set_age(self):
        today = date.today()
        age = relativedelta(today, self.birthdate).years

        self._validate_age(age)

        self.age = age
        
    def _validate_age(self, age):
        if age < 18: raise ValidationError()


class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='status')
    is_online = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {'Online' if self.is_online else 'Offline'}"

