from django.urls import path, include
from rest_framework import routers
from apps.core import views as core_views

router = routers.DefaultRouter()
router.register(r'example', core_views.ExampleViewSet, basename='example')

urlpatterns = [
    path('', include(router.urls)),
]
