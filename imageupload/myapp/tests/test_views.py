from django.test import TestCase, Client
from django.urls import reverse, resolve
from myapp.models import Tier, Size, Image, Profile, ExpiringLink
from django.contrib.auth import get_user_model
import json

# class UpdateImageAPIView(APIView):
# class GenerateExpiringLinkAPIView(APIView):
# def validate_expiring_link(request, pk, size):   

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)
        self.image = Image.objects.create(
            owner=self.user,
            title='Test Image',
            description='A test image',
         )
        self.size = Size.objects.create(size = 400)
        self.tier = Tier.objects.create(tier='Enterprise')
        self.tier.sizes.set([self.size])
        self.profile = Profile.objects.create(user=self.user, tier=self.tier)
        
    def test_login_user_view(self):
        response = self.client.get(reverse('images'))
        self.assertEquals(response.status_code, 200)

    def test_logout_user_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 200)

    def test_upload_image_view(self):
        with open('static/images/desktop_wallpaper.jpg', 'rb') as image_file:
            response = self.client.post(reverse('upload_image'), {
                'image': image_file,
                'title': 'Uploaded Image',
                'description': 'An uploaded image',
            })
        self.assertEquals(response.status_code, 200)

    def test_images_list_view(self):
        response = self.client.get(reverse('images')) 
        self.assertEquals(response.status_code, 200)

    def test_delete_image_view(self):
        response = self.client.get(reverse('delete_image', args=[self.image.id]))
        self.assertEqual(response.status_code, 200)

