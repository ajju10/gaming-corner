from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_us, name='contact_us'),
    path('organize/new', views.organize_new, name='organize_tournament'),
    path('my-tournaments/', views.my_tournaments, name='my_tournaments'),
    path('my-tournaments/delete/<tournament_id>/', views.delete, name='delete'),
    path('browse/', views.browse, name='browse'),
    path('tournament/details/<tournament_id>/', views.details, name='details'),
    path('tournament/join/<tournament_id>', views.join_tournament, name='join'),
]
