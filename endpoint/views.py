from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from .models import VideoResponse
from upload import views as upload_views
from upload.models import User

_OFFSET_DEFAULT = 0
_OFFSET_DEFAULT_S = str(_OFFSET_DEFAULT)

_SLICE_SIZE_MAX = 1000
_SLICE_SIZE_DEFAULT = 10
_SLICE_SIZE_DEFAULT_S = str(_SLICE_SIZE_DEFAULT)


def _clamp(n, a, b):
    low, high = sorted([a, b])
    return max(low, min(high, n))


def _get_pagination(request, prefix=''):

    offset_param = '{}offset'.format(prefix)
    limit_param = '{}limit'.format(prefix)

    offset_value = request.GET.get(offset_param, _OFFSET_DEFAULT_S)
    limit_value = request.GET.get(limit_param, _SLICE_SIZE_DEFAULT_S)

    offset = max(int(offset_value), _OFFSET_DEFAULT)
    limit = _clamp(int(limit_value), 1, _SLICE_SIZE_MAX)

    return offset, limit


def _get_pagination_range(request, prefix=''):

    offset, limit = _get_pagination(request, prefix)

    return offset, offset + limit


def get_videos_by_user(request, username):

    video_objects = VideoResponse.objects.filter(author=username).values()

    return JsonResponse(list(video_objects), safe=False)


def get_responses_to_video(request, video_id):

    responses = VideoResponse.objects.filter(response_to__id=video_id).values()

    return JsonResponse(list(responses), safe=False)


def latest_topics(request):

    start, end = _get_pagination_range(request)

    topics = VideoResponse.objects.filter(
        response_to__isnull=True,
    ).order_by(
        '-date_added',
    ).values()[start:end]

    return JsonResponse(list(topics), safe=False)


def latest_responses(request):

    start, end = _get_pagination_range(request)

    responses = VideoResponse.objects.filter(
        response_to__isnull=False,
    ).order_by(
        '-date_added',
    ).values()[start:end]

    return JsonResponse(list(responses), safe=False)


def response_points(request, video_id):

    responses = VideoResponse.objects.filter(response_to__id=video_id).values(
        'playback_start_at'
    ).distinct()

    points = [
        r['playback_start_at'] for r in responses
    ]

    return JsonResponse(points, safe=False)


def response_point_detail(request, video_id, point):

    responses = VideoResponse.objects.filter(
        response_to__id=video_id,
        playback_start_at=point,
    ).values(
        'id',
        'title',
        'filename',
        'thumbnail',
        'author',
    )

    return JsonResponse(list(responses), safe=False)


@csrf_exempt
def upload_video(request):
    user = User.objects.all()[0]
    upload_views.handle_upload(request, user)
    return JsonResponse({})


def video(request, video_id):

    video = VideoResponse.objects.filter(id=video_id).values().get()

    return JsonResponse(video, safe=False)
