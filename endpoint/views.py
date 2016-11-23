from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from    .models import VideoResponse


def get_videos_by_user(request, username):
    video_objects =  VideoResponse.objects.filter(author=username)
    # print(video_objects)
    return JsonResponse(serializers.serialize('json', video_objects), safe=False)

def get_responses_to_video(request, video_id):

    topic_video =  VideoResponse.objects.get(id=video_id)

    responses = VideoResponse.objects.filter(response_to=topic_video)

    return JsonResponse(serializers.serialize('json', responses), safe=False)

