from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('organize/new/', views.organize_new, name='organize_tournament'),
    path('my_tournaments/', views.my_tournaments, name='my_tournaments'),
    path('my_tournaments/delete/<tournament_id>/', views.delete, name='delete'),
    path('browse/', views.browse, name='browse'),
    path('tournament/register/<tournament_id>/', views.register, name='register'),
]
