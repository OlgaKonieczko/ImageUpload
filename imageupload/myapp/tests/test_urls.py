from django.test import SimpleTestCase
from django.urls import reverse, resolve
from myapp.views import image, images, deleteImage, validate_expiring_link
from myapp.views import loginUserAPIView, UserLogoutViewAPI, UploadImageAPIView, UpdateImageAPIView, GenerateExpiringLinkAPIView

class TestUrls(SimpleTestCase):

    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, loginUserAPIView)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, UserLogoutViewAPI)

    def test_images_url_is_resolved(self):
        url = reverse('images')
        self.assertEquals(resolve(url).func, images)

    def test_image_url_is_resolved(self):
        url = reverse('image', args=['arg1', 'arg2'])
        self.assertEquals(resolve(url).func, image)

    def test_upload_image_url_is_resolved(self):
        url = reverse('upload_image')
        self.assertEquals(resolve(url).func.view_class, UploadImageAPIView)

    def test_update_image_url_is_resolved(self):
        url = reverse('update_image', args=['arg1'])
        self.assertEquals(resolve(url).func.view_class, UpdateImageAPIView)

    def test_delete_image_url_is_resolved(self):
        url = reverse('delete_image', args=['arg1'])
        self.assertEquals(resolve(url).func, deleteImage)     

    def test_generate_link_url_is_resolved(self):
        url = reverse('generate_exp_link', args=['arg1', 'arg2'])
        self.assertEquals(resolve(url).func.view_class, GenerateExpiringLinkAPIView)      

    def test_generate_link_url_is_resolved(self):
        url = reverse('exp_link', args=['arg1', 'arg2'])
        self.assertEquals(resolve(url).func, validate_expiring_link)                     