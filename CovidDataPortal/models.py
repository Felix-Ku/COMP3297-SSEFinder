from django.contrib.auth.models import User
from django.db import models


# Create your models here.
# class Location_data(models.Model):
#     name = models.CharField(max_length=200)
#     Pop = models.IntegerField()
#     api = models.CharField(max_length=1000)
#     url = models.CharField(max_length=1000)
#     def __str__(self): # Add string functions to models
#         return self.name

class cases(models.Model):
    case_number = models.IntegerField(primary_key=True)
    person_name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=10, unique=True)
    birth_date = models.DateField()
    symptoms_date = models.DateField()
    confirmation_date = models.DateField()

    def __str__(self): # Add string functions to models
        return self.name
