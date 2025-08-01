from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def search_page_view(request):
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Search across multiple models
        users = User.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query) |  Q(username__icontains=query)
        )
        
        # Combine results
        results = list(users)
    
    # Pagination
    paginator = Paginator(results, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': 'Spectrum Date',
        'query': query,
        'results': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    
    return render(request, 'core/search_page.html', context)