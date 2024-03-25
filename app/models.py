from django.db import models


# Create your models here.
def _str_(self):
    return self.name


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    CNIC = models.CharField(max_length=14, unique=True)
    phone = models.CharField(max_length=13, unique=True)

class Accounts(models.Model):
    SAVING = 'Saving'
    CURRENT = 'Current'
    FIXED_DEPOSIT = 'Fixed Deposit'

    ACCOUNT_TYPE_CHOICES = [
        (SAVING, 'Saving'),
        (CURRENT, 'Current'),
        (FIXED_DEPOSIT, 'Fixed Deposit'),
    ]

    ACTIVE = 'Active'
    INACTIVE = 'Inactive'

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=100, unique=True)
    balance = models.FloatField()
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default=CURRENT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)