from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Location_data(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self): # Add string functions to models
        return self.name

class cases(models.Model):
    case_number = models.IntegerField(unique=True)
    person_name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=10, unique=True)
    birth_date = models.DateField()
    symptoms_date = models.DateField()
    confirmation_date = models.DateField()

    def __str__(self): # Add string functions to models
        return self.case_number

class case_records(models.Model):
    case_number = models.IntegerField()
    person_name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=10)
    birth_date = models.DateField()
    symptoms_date = models.DateField()
    confirmation_date = models.DateField()

    def __str__(self): # Add string functions to models
        return self.case_number

class case_recordss(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):  # Add string functions to models
        return self.name
