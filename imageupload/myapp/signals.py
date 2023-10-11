from django.contrib.auth.models import User
from .models import Profile, Image, Tier
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            tier = Tier.objects.get(tier='Basic')
        )

def updateProfile(sender, instance, created, **kwargs):
    profile = instance
    user=profile.user
    if not created:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
        
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()

def updateImage(sender, instance, created, **kwargs):
    if not created:
        profile = instance
        tier=profile.tier
        images = Image.objects.filter(owner=profile.user)
        for image in images:
                image.tier = tier
                image.save()


post_save.connect(createProfile, sender=User)
post_save.connect(updateProfile, sender=Profile)
post_save.connect(updateImage, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)    