from django.db import models
from django.contrib.auth.models import User

# Create your models here


class UserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extension')
    phone = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    intro = models.TextField()
    stuff_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class Customer(models.Model):
    name = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=11)
    email = models.EmailField()
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('indoor', 'indoor'),
        ('out door', 'out door')
    )

    name = models.CharField(max_length=30)
    price = models.CharField(max_length=10)
    category = models.CharField(max_length=30, choices=CATEGORY)
    description = models.CharField(max_length=100, blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('pending', 'pending'),
        ('out of delivery', 'out of delivery'),
        ('delivered', 'delivered')
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='c_order')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='p_order')
    time_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS)
