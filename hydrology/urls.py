from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('record/', views.record, name = 'record'),
    path('category/', views.search_hydropost_type, name = 'category'),
]
