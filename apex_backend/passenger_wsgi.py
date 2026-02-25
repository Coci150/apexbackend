import os
import sys

# Add your project directory to the sys.path
project_home = '/home/RikoNaito/apexbackend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apex_backend.settings')

# Import Django's WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
