from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('bands/', views.band_list, name='band_list'),
    path('bands/<slug:slug>/', views.band_detail, name='band_detail'),
    path('releases/<slug:slug>/', views.release_detail, name='release_detail'),
    path('fanzines/<slug:slug>/', views.fanzine_detail, name='fanzine_detail'),
    path('labels/<slug:slug>/', views.label_detail, name='label_detail'),
    path('search/', views.search, name='search'),
    path('admin/core/link/review/', views.review_queue, name='review_queue'),
]
