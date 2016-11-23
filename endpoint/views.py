from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from    .models import VideoResponse


def get_videos_by_user(request, username):
    video_objects =  VideoResponse.objects.filter(author=username)    print(video_objects)
    return JsonResponse(serializers.serialize('json', video_objects), safe=False)
