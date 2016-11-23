from django.conf.urls import url
from .views import get_videos_by_user

urlpatterns = [
    url(r'by_author/(?P<username>[a-z0-9]*)', get_videos_by_user, name='get_by_user'),

]