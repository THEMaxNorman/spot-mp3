from __future__ import unicode_literals



from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
 # the profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    isAdmin = models.BooleanField(default=False)
    hasPaid = models.BooleanField(default=False)




@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()