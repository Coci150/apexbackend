# apex_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from core.admin import ContactAdmin
from core.views import campaign_stats_view  # Import the wrapper view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # Fix the stats URL by wrapping the admin view
    path('stats/', campaign_stats_view, name='campaign-stats'),
    ]
