from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('bands/', views.band_list, name='band_list'),
    path('bands/<slug:slug>/', views.band_detail, name='band_detail'),
    path('releases/<slug:slug>/', views.release_detail, name='release_detail'),
    path('search/', views.search, name='search'),
]