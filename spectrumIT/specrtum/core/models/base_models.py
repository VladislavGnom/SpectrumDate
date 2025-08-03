from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.dateparse import parse_date
from django.forms import ValidationError


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
            self._set_age(self)
        super().save(*args, **kwargs)

    def _set_age(self):
        if isinstance(self.birthdate, str):
            self.birthdate = parse_date(self.birthdate)

        row_age = timesince(parse_date(self.birthdate), timezone.now().date())
        age = row_age.split()[0]

        self._validate_age(age)

        self.age = age
        
    def _validate_age(age):
        if age < 18: raise ValidationError()

    # def save(self, *args, **kwargs):
    #     self.birthdate = timezone.make_aware(self.birthdate)
    #     today = timezone.make_aware(timezone.now())
    #     age = today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
    #     self.age = age
    #     super().save(*args, **kwargs)
