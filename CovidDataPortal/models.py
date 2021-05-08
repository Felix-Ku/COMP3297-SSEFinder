from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Location_data(models.Model):
    name = models.CharField(max_length=200)
    Pop = models.IntegerField()
    api = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)
    def __str__(self): # Add string functions to models
        return self.name

class cases(models.Model):
    case_number = models.IntegerField()
    # person_name = models.CharField(max_length=50)
    # id_number = models.CharField(max_length=10, unique=True)
    # birth_date = models.DateTimeField()
    # symptoms_date = models.DateTimeField()
    # confirmation_date = models.DateTimeField()

    def __str__(self): # Add string functions to models
        return self.case_number
