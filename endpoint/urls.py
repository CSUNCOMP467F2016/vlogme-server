from django.conf.urls import url
from . import views as v


urlpatterns = [
    url(r'by_author/(?P<username>[a-z0-9]*)', v.get_videos_by_user, name='get_by_user'),
    url(r'get_responses_to_video/(?P<video_id>[0-9]*)', v.get_responses_to_video, name='get_responses_to_video'),
    url(r'response-points/(?P<video_id>[0-9]*)', v.response_points, name='response_points'),
]
