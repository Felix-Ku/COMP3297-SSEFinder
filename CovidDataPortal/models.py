from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Location_data(models.Model):
    name = models.CharField(max_length=200)
    Pop = models.IntegerField()
    api = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)
    def __str__(self): # Add string functions to models
        return self.name

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ID = models.CharField(max_length=30, blank=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()