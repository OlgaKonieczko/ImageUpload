from django.urls import path
from . import views
from .views import (
	loginUserAPIView,
    UserLogoutViewAPI
)
urlpatterns = [
    path("", loginUserAPIView.as_view(), name='login'),
    path("logout/", UserLogoutViewAPI.as_view(), name='logout'),
    path("images/", views.images, name='images'),
    path("images/<str:pk>/<str:size>", views.image, name='image'),
    path("upload/", views.upload, name='upload'),
]