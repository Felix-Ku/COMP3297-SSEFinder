from django.contrib.auth.models import User
from django.db import models

class case_record(models.Model):
    case_number = models.IntegerField()
    person_name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=255)
    birth_date = models.DateField()
    symptoms_date = models.DateField()
    confirmation_date = models.DateField()

    def __str__(self): # Add string functions to models
        return self.case_number

class attendances(models.Model):
    venue_name = models.CharField(max_length=100)
    venue_location = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    hk_grid = models.CharField(max_length=50)
    event_date = models.DateField()
    description = models.CharField(max_length=200)

    def __str__(self): # Add string functions to models
        return self.venue_name
