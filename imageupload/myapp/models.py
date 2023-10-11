from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
import secrets
import uuid

class Size(models.Model):
    size = models.IntegerField(null=False, blank=False)
    description  = models.TextField(blank = True, null = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.size)
    
class Tier(models.Model):
    tier = models.CharField(max_length=200, blank = False, null = False)
    description  = models.TextField(blank = True, null = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    sizes = models.ManyToManyField(Size, blank = True)  
    generate_expiring_link = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.tier)
    

class Image(models.Model):
    image = models.ImageField(blank = True, null = True, upload_to='')
    owner= models.ForeignKey(User, on_delete=models.CASCADE, blank = False, null = False)
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True)
    description  = models.TextField(blank = True, null = True)
    title = models.CharField(max_length=200, blank = True, null = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
     

    def __str__(self):
        return str(self.title)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    username = models.CharField(max_length=200, null = True, blank = True)
    name = models.CharField(max_length=200, blank = True, null = True)
    email = models.EmailField(max_length=500, blank = True, null = True)
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True) 
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)
    

class ExpiringLink(models.Model):
    resource = models.ForeignKey(Image, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, unique=True)
    expiration_timestamp = models.DateTimeField()    

    @staticmethod
    def generate_link(resource, expiration_seconds):
        expiration_timestamp = timezone.now() + timedelta(seconds=expiration_seconds)
        token = secrets.token_hex(16)
        ExpiringLink.objects.create(resource=resource, token=token, expiration_timestamp=expiration_timestamp)
        return token
