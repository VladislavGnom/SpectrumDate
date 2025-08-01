# from django.contrib.gis.db.models.functions import Distance
# from django.contrib.gis.measure import D
from core.models.slider_models import Swipe
from core.models.base_models import User

def get_recommendations(user, max_distance_km=50, limit=10):
    """
    Подбор кандидатов на основе:
     - местоположения (если есть)
     - общих интересов
     - непросмотренных ранее
    """
    # user_profile = user.userprofile

    swiped_users = Swipe.objects.filter(swiper=user).values_list('swiped_on', flat=True)

    recommendations = User.objects.exclude(id=user.id).exclude(id__in=swiped_users)

    # some logic of recommendations

    return recommendations[:limit]
