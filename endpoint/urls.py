from django.conf.urls import url
from .views import get_videos_by_user, get_responses_to_video

urlpatterns = [
    url(r'by_author/(?P<username>[a-z0-9]*)', get_videos_by_user, name='get_by_user'),
    url(r'get_responses_to_video/(?P<video_id>[0-9]*)', get_responses_to_video, name='get_responses_to_video'),

]