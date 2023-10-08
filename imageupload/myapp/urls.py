from django.urls import path
from . import views
from .views import (
	loginUserAPIView,
    UserLogoutViewAPI,
    UploadImageAPIView,
    UpdateImageAPIView
)
urlpatterns = [
    path("", loginUserAPIView.as_view(), name='login'),
    path("logout/", UserLogoutViewAPI.as_view(), name='logout'),
    path("images/", views.images, name='images'),
    path("images/<str:pk>/<str:size>", views.image, name='image'),
    path("upload/", UploadImageAPIView.as_view(), name='upload_image'),
    path("update/<str:pk>", UpdateImageAPIView.as_view(), name='update_image'),
    path("delete/<str:pk>", views.deleteImage, name='delete_image')        
]