from django.db import models
from django.contrib.auth.models import User
from menu.models import Food

# Create your models here.
class RestaurantTable(models.Model):
    table_number = models.PositiveIntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.table_number)

ORDER_STATUS = [
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("preparing", "Preparing"),
    ("ready", "Ready"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="Pending")

    def __str__(self):
            return str(self.user)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.order)

