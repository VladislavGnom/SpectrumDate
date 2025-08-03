from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import AnonymousUser
from core.models.base_models import User
from core.forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)    
            return redirect('main')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})
