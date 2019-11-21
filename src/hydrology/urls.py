from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from hydrology import views
from hydrology.views import HydropostViewSet

urlpatterns = [
    path('observation/', views.observation, name='observation'),
    path('category/', views.search_hydropost_category, name='category'),
    path('record/', views.record, name='record'),
    path('data/', views.data, name='data'),
    path('', views.home, name='home'),
]

router = DefaultRouter(trailing_slash=False)
router.register(r'hydroposts', HydropostViewSet)

urlpatterns = urlpatterns + router.urls
