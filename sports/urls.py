from django.urls import path
from . import views

app_name = 'sports'

urlpatterns = [
    # Sport URLs
    path('sports/', views.sport_list, name='sport-list'),
    path('sports/<int:pk>/', views.sport_detail, name='sport-detail'),
    
    # Registration URLs
    path('registrations/', views.registration_list, name='registration-list'),
    path('registrations/<int:pk>/', views.registration_detail, name='registration-detail'),
    
    # Team URLs
    path('teams/', views.team_list, name='team-list'),
    path('teams/<int:pk>/', views.team_detail, name='team-detail'),
]