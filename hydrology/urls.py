from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views



urlpatterns = [
    path('', views.home, name = 'home'),
    path('category/', views.search_hydropost_type, name = 'category'),
    path('record/', views.record, name = 'record'),
]
