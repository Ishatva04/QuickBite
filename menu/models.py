from django.db import models

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