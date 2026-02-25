from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.contact_submit, name='contact'),
    path('newsletter/', views.newsletter_subscribe, name='newsletter'),
    path('health/', views.health_check, name='health'),
]