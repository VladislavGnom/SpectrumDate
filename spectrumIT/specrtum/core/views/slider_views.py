from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, HttpResponseNotFound
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from core.utils.utils import get_cur_user, get_user_by_id
from core.utils.recommendations_logic import get_recommendations
from core.utils.chat_utils import record_swipe

def load_another_user(request: HttpRequest):
    cur_user = get_cur_user(request)
    users = get_recommendations(cur_user)

    paginator = Paginator(users, 1) 
    page_number = request.GET.get('page')


    page_obj = paginator.get_page(page_number)

    if not page_number or not page_obj: return HttpResponseNotFound()

    if page_obj.has_next():
        next_page = page_obj.next_page_number()
    else:
        next_page = None

    data = {
        'user': list(page_obj.object_list.values())[0] if page_obj.object_list else None,
        'has_next': page_obj.has_next(),
        'next_page': next_page,
        'debug': {  # Добавьте эту информацию для отладки
            'total_users': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': page_obj.number,
        }
    }

    return JsonResponse(data)


@login_required
def slider(request: HttpRequest):
    # currentPage = request.GET.get('page', 1)
    # user_data = requests.get(request.build_absolute_uri(f'/load-another-user?page={currentPage}'))

    context = {
        'title': 'Spectrum Date',
        # 'user': user_data,
    }

    return render(request, 'core/slider_page.html', context=context)

@login_required
def slider_by_id(request: HttpRequest, user_id=None):

    # currentPage = request.GET.get('page', 1)
    # user_data = requests.get(request.build_absolute_uri(f'/load-another-user?page={currentPage}'))
    if not user_id: return HttpResponseNotFound("Ошибка! Не найдено")

    user_data = get_user_by_id(user_id)

    context = {
        'title': 'Spectrum Date',
        'slider_of_user': user_data,
    }

    return render(request, 'core/user_form_page.html', context=context)

@login_required
def record_swipe_view(request: HttpRequest):
    request_data = request.GET

    swiped_on_user_id = request_data.get('swiped_on')
    liked = request_data.get('liked')
    cur_user = get_cur_user(request)
    swiped_on_user = get_user_by_id(swiped_on_user_id)

    record_swipe(
        swiper=cur_user,
        swiped_on=swiped_on_user,
        liked=liked
    )
    
    return JsonResponse({'status': 200})
