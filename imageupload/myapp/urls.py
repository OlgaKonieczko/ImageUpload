from django.urls import path
from . import views
from .views import (
	loginUserAPIView,
    UserLogoutViewAPI,
    UploadImageAPIView,
    UpdateImageAPIView,
    GenerateExpiringLinkAPIView,
)
urlpatterns = [
    path("", loginUserAPIView.as_view(), name='login'),
    path("logout/", UserLogoutViewAPI.as_view(), name='logout'),
    path("images/", views.images, name='images'),
    path("images/<str:pk>/<str:size>", views.image, name='image'),
    path("upload/", UploadImageAPIView.as_view(), name='upload_image'),
    path("update/<str:pk>", UpdateImageAPIView.as_view(), name='update_image'),
    path("delete/<str:pk>", views.deleteImage, name='delete_image'),     
    path("generate_exp_link/<str:pk>/<str:size>", GenerateExpiringLinkAPIView.as_view(), name='generate_exp_link'),
    path("exp_link/<str:pk>/<str:size>", views.validate_expiring_link, name='exp_link')
]

