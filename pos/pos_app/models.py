from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class TableUser(models.Model):
    ROLE_CHOICES = (
        ('user', 'user'),
        ('admin', 'admin')
    )

    username = models.CharField(max_length=200, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255, null=False, blank=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username

class TableOrder(models.Model):
    PACKAGE_CHOICES = (
        ('Wash and Fold', 'Wash and Fold'),
        ('Wash, Dry and Fold', 'Wash, Dry and Fold'),
        ('Wash, Dry, Iron and Fold', 'Wash, Dry, Iron and Fold'),
    )

    STATUS_CHOICES = (
        ('Waiting..', 'Waiting..'),
        ('In Process..', 'In Process..'),
        ('Ready for Pickup..', 'Ready for Pickup..'),
        ('Delivered..', 'Delivered..'),
    )

    packages = models.CharField(max_length=50, choices=PACKAGE_CHOICES, default='Wash and Fold')
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    status_order = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Waiting..')
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('TableUser', on_delete=models.CASCADE)

    def get_price(self):
        price_choices = {
            'Wash and Fold': 20000,
            'Wash, Dry and Fold': 25000,
            'Wash, Dry, Iron and Fold': 35000,
        }
        return price_choices.get(self.packages, 0)
