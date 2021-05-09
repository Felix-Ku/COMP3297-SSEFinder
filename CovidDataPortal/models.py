from django.contrib.auth.models import User
from django.db import models

class attendances(models.Model):
    venue_name = models.CharField(max_length=100)
    venue_location = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    hk_grid = models.CharField(max_length=50)
    event_date = models.DateField()
    description = models.CharField(max_length=200)

    def __str__(self): # Add string functions to models
        return str(self.id)

class case_records(models.Model):
    case_number = models.IntegerField()
    person_name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=255)
    birth_date = models.CharField(max_length=255)
    symptoms_date = models.CharField(max_length=255)
    confirmation_date = models.CharField(max_length=255)

    def __str__(self): # Add string functions to models
        return str(self.case_number)

    class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staffnum = models.IntegerField(max_length=6, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.EmailField(max_length=254)

    def __str__(self):
        return f'{self.user.username} - Personal Info'
