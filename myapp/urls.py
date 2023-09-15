from django.urls import path
from . import views

urlpatterns = [
        path("", views.index, name="index"),
        path("spam-detector/", views.evaluate_message, name="spam-detector"),
]
