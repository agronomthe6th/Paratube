"""
WSGI config for youtube_python project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from static_ranges import Ranges
from whitenoise import Cling, MediaCling

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_python.settings')

application = Ranges(Cling(MediaCling(get_wsgi_application())))

