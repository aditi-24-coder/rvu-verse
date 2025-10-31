"""
WSGI config for rvuverse project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rvuverse.settings')

application = get_wsgi_application()

# Set the application to run on port 8000
if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(["", "runserver", "0.0.0.0:8000"])
