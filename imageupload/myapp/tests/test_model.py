from django.test import TestCase, Client
from django.utils import timezone 
from django.contrib.auth import get_user_model
from myapp.models import Image, ExpiringLink, Profile, Size, Tier


class TestModels(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.filter(user = self.user)
        self.size = Size.objects.create(size = 400)
        self.tier = Tier.objects.create(tier='Enterprise', generate_expiring_link = True)
        self.profile.tier = self.tier
        self.tier.sizes.set([self.size])
        self.image = Image.objects.create(
            owner=self.user,
            title='Test Image',
            description='A test image'
         )
        
    def test_generate_exp_links(self):
        ExpiringLink.objects.create(
            token='test_token',
            expiration_timestamp=timezone.now() + timezone.timedelta(hours=1), 
            resource =  self.image
        )
        token = ExpiringLink.generate_link(self.image, 350)
        expiring_link = ExpiringLink.objects.get(token=token)
        self.assertEqual(expiring_link.resource, self.image)
        self.assertTrue(token)
