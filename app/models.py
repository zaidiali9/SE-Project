from django.db import models

# Create your models here.
def _str_(self):
    return self.name

class User  (models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    CNIC = models.CharField(max_length=14, unique=True)
    phone = models.CharField(max_length=13,unique=True)
    
