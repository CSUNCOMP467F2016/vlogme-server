"""
WSGI config for file_upload project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os,sys
sys.path.append('/opt/bitnami/apps/django/django_projects/Project/comp467_upload')
os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/Project/comp467_upload/egg_cache")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "file_upload.settings")

application = get_wsgi_application()
