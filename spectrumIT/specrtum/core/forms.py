from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models.base_models import User
from datetime import date
from dateutil.relativedelta import relativedelta


class RegisterForm(UserCreationForm):
    MIN_AGE = 18

    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'gender', 'birthdate']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if not birthdate:
            raise forms.ValidationError("Пожалуйста, укажите дату рождения")
        
        today = date.today()
        age = relativedelta(today, birthdate).years

        if age < self.MIN_AGE:
            raise forms.ValidationError(f"Вам должно быть не менее {self.MIN_AGE} лет для регистрации")

        return birthdate
