from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth import get_user_model

User = get_user_model()

def main_page_view(request: HttpRequest):
    context = {
        'title': 'Spectrum Date'
    }

    return render(request, 'core/main_page.html', context=context)
