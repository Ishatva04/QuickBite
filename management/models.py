from django.db import models
from django.contrib.auth.models import User
from menu.models import Food
from django.utils import timezone

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
    estimated_preparation_time = models.PositiveIntegerField(default=15)
    preparing_started_at = models.DateTimeField(null=True,blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="pending")

    def __str__(self):
            return str(self.user)
    def save(self, *args, **kwargs):

        if self.status == "preparing" and self.preparing_started_at is None:
            self.preparing_started_at = timezone.now()

        super().save(*args, **kwargs)



class Payment(models.Model):

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )

    razorpay_order_id = models.CharField(
        max_length=100
    )

    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    razorpay_signature = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        default="created"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Payment for Order #{self.order.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.order)

