from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models.base_models import User


class RegisterForm(UserCreationForm):
    # email = forms.EmailField(required=True)

    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'gender', 'birthdate']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }
