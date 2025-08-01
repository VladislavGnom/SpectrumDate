from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import AnonymousUser
from core.models.base_models import User

def register(request):
    if request.user is AnonymousUser:
        return redirect('main')
    
    if request.method == 'POST':
        data = request.POST

        user = User.objects.create_user(
            username=data.get('username'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            age=data.get('age'),
            password=data.get('password'),
            gender=data.get('gender'),
            birthdate=data.get('birthdate'),
            location=data.get('location')
        ) 

        if user:
            login(request, user)    
            return redirect('main')

    return render(request, 'registration/register.html')
