from django.urls import path
from . import views

urlpatterns = [
        path("", views.index, name="index"),
        path("spam-detector/", views.evaulate_message, name="spam-detector"),
]
