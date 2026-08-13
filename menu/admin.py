from django.contrib import admin
from .models import Category, Food


admin.site.register(Category)


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_available")