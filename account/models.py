from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.
class User(AbstractUser):
    staff_number = models.CharField(blank=True, null=True, max_length=6, validators=[RegexValidator(r'^\d{1,10}$')])
