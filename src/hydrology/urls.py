from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('observation/', views.observation, name = 'observation'),
    path('category/', views.search_hydropost_category, name = 'category'),
    path('record/', views.record, name = 'record'),
    path('data/', views.data, name = 'data'),
    path('', views.home, name = 'home'),
]
