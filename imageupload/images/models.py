from django.db import models
from django.contrib.auth.models import User
from users.models import Tier
import uuid

# Create your models here.
class Size(models.Model):
    tier = models.ManyToManyField(Tier, blank = False)
    size = models.IntegerField(null=False, blank=False)
    description  = models.TextField(blank = True, null = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.tier)
    

class Image(models.Model):
    #image = models.ImageField(blank = True, null = True, upload_to='/', default = '')
    owner= models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    description  = models.TextField(blank = True, null = True)
    name = models.CharField(max_length=200, blank = True, null = True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)
    