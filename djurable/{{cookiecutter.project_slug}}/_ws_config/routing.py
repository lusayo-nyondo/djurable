from django.urls import path
from apps.core import consumers as core_consumers

websocket_urlpatterns = [
    path('ws/example/', core_consumers.ExampleConsumer.as_asgi()),
]
