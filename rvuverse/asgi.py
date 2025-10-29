"""
ASGI config for rvuverse project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rvuverse.settings')

application = get_asgi_application()
