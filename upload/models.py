from django.contrib.auth.models import User
from django.db import models

class ResponseFile(models.Model):
    user = models.ForeignKey(User, related_name='user')
    docfile = models.FileField(upload_to='temp/')
