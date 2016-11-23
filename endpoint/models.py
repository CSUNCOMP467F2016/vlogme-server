from django.db import models


class VideoResponse(models.Model):

    id = models.AutoField(primary_key=True)
    author = models.CharField(max_length=20, blank=True)
    title = models.CharField(max_length=200, blank=True)
    filename = models.CharField(max_length=100, blank=True)
    thumbnail = models.CharField(max_length=100, blank=True)
    playlist_file = models.CharField(max_length=100, blank=True)
    response_to = models.ForeignKey('self',null=True, blank=True, default=None, on_delete=models.CASCADE)
    playback_start_at = models.IntegerField(default=0)
    length = models.CharField(max_length=20, blank= True)
    date_added = models.DateTimeField(auto_now_add=True)
    original_filename = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title