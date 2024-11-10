from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    STATUS_CHOICES = {True: 'Selling', False: 'Out of stock'}
    CATEGORY_CHOICES = {
        'machinery': 'Machinery',
        'grain': 'Grain',
        'property': 'Property',
        'others': 'Others',
    }

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default='others')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    status = models.BooleanField(choices=STATUS_CHOICES, default=True)
    location = models.CharField(max_length=255)
    stock = models.PositiveIntegerField(default=0)
    createAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True , on_delete=models.CASCADE)  

    def __str__(self):
        return self.name

