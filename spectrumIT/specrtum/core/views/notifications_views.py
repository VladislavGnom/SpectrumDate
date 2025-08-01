from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from core.models.slider_models import UserMessageStorage
from core.utils.utils import get_cur_user, get_user_by_id


def create_user_notification(request: HttpRequest, user_id: int):
    # if request.method == 'GET': return HttpResponseBadRequest

    target_user = get_user_by_id(user_id)
    message = request.GET.get('message')

    if not message: return JsonResponse({'status': 500})

    created_message = UserMessageStorage.objects.create(
        target_user=target_user,
        message=message,
    )
    
    if created_message:
        return JsonResponse({'status': 200})
    else:
        return JsonResponse({'status': 500})
    
@login_required
def user_notifications(request):
    cur_user = get_cur_user(request)
    user_notifications = UserMessageStorage.objects.filter(target_user=cur_user)

    context = {
        'title': 'SpectrumDate - Notifications',
        'notifications': user_notifications,
    }

    return render(request, 'core/show_notifications_page.html', context=context) 
