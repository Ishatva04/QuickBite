from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
                return self.name

SPICY_LEVELS = [
    ("not_spicy", "Not Spicy"),
    ("mild", "Mild"),
    ("medium", "Medium"),
    ("spicy", "Spicy"),
]

class Food(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )

    name = models.CharField(max_length=100)

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    is_available = models.BooleanField(default=True)

    description = models.TextField(blank=True)

    ingredients = models.TextField(blank=True)

    spicy_level = models.CharField(
        max_length=20,
        choices=SPICY_LEVELS,
        blank=True
    )

    image = models.ImageField(
        upload_to="food/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="Pending")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)