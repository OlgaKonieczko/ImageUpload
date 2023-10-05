from django.urls import path
from . import views

urlpatterns = [
    path("", views.images, name='images'),
    path("<str:pk>", views.image, name='image'),
    path("upload/", views.images, name='upload'),
]