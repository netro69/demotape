from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.BandListView.as_view(), name='band_list'),
    path('<slug:slug>/', views.BandDetailView.as_view(), name='band_detail'),
]
