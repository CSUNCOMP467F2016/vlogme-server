from django.http import HttpResponse, JsonResponse
from django.core import serializers

from .models import VideoResponse


def get_videos_by_user(request, username):

    video_objects = VideoResponse.objects.filter(author=username)

    return HttpResponse(
        serializers.serialize('json', video_objects),
        content_type='application/json',
    )


def get_responses_to_video(request, video_id):

    topic_video = VideoResponse.objects.get(id=video_id)
    responses = VideoResponse.objects.filter(response_to=topic_video)

    return HttpResponse(
        serializers.serialize('json', responses),
        content_type='application/json',
    )


def latest_topics(request):
    return HttpResponse(
        '[]',
        content_type='application/json',
    )


def latest_responses(request):
    return HttpResponse(
        '[]',
        content_type='application/json',
    )


def response_points(request, video_id):

    responses = VideoResponse.objects.filter(response_to__id=video_id)

    points = [
        r.playback_start_at for r in responses
    ]

    return JsonResponse(points, safe=False)
