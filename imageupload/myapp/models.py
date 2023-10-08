from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
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
    owner= models.ForeignKey(User, on_delete=models.CASCADE)
    description  = models.TextField(blank = True, null = True)
    title = models.CharField(max_length=200, blank = True, null = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.id)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=200, null = True, blank = True)
    name = models.CharField(max_length=200, blank = True, null = True)
    email = models.EmailField(max_length=500, blank = True, null = True)
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null = True, blank = True) 
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)
    