from django.db import models
from django.utils import timezone

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


class ATMcards(models.Model):
    VISA = 'Visa'
    MASTERCARD = 'Mastercard'
    AMERICAN_EXPRESS = 'American Express'

    CARD_TYPE_CHOICES = [
        (VISA, 'Visa'),
        (MASTERCARD, 'Mastercard'),
        (AMERICAN_EXPRESS, 'American Express'),
    ]
    accounts = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16, unique=True)
    pin = models.CharField(max_length=4)
    expiry_date = models.DateField()
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES)
    is_active = models.BooleanField(default=False)


class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20)  # e.g., 'Deposit', 'Withdrawal', 'Transfer'
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now) 