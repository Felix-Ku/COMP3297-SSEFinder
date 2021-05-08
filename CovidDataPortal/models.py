from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Location_data(models.Model):
    name = models.CharField(max_length=200)
    Pop = models.IntegerField()
    api = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)
    def __str__(self): # Add string functions to models
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')

    number = models.CharField('CHP staff number', max_length=6, blank=True)

    class Meta:
        verbose_name = 'User profile'

    def __str__(self):
        # return self.user.__str__()
        return "{}".format(self.user.__str__())