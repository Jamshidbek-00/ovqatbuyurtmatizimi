from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )

    username = None 
    phone = models.CharField(max_length=13, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone




class Food(models.Model):
    TYPE_CHOICES = (
        ('ovqat', 'Ovqat'),
        ('ichimlik', 'Ichimlik'),
        ('shirinlik', 'Shirinlik'),
    )

    nomi = models.CharField(max_length=100)
    narxi = models.PositiveIntegerField()
    turi = models.CharField(max_length=50, choices=TYPE_CHOICES)
    mavjud = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nomi





class Order(models.Model):
    STATUS_CHOICES = (
        ('yangi', 'Yangi'),
        ('tayyorlanmoqda', 'Tayyorlanmoqda'),
        ('yetkazilmoqda', 'Yetkazilmoqda'),
        ('yetkazildi', 'Yetkazildi'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    manzil = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='yangi')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Order {self.id} by {self.user.phone}"




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    @property
    def total_price(self):
        return self.food.narxi * self.count

    def __str__(self):
        return f"{self.food.nomi} * {self.count}"