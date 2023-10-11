from django.contrib import admin
from .models import Tier, Size, Image, Profile, ExpiringLink

admin.site.register(Tier)
admin.site.register(Size)
admin.site.register(Image)
admin.site.register(Profile)
admin.site.register(ExpiringLink)