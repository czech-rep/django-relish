# part 8, 27:20 min
from django.db.models.signals import post_save 
    # signal fired when obj (User) is saved
    
from django.contrib.auth.models import User # = sender = he gets created
from django.dispatch import receiver

from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()