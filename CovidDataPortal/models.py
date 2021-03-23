from django.db import models

# Create your models here.
class Location_data(models.Model):
    name = models.CharField(max_length=200)
    Pop = models.IntegerField()
    api = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)
    def __str__(self): # Add string functions to models
        return self.name