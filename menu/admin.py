from django.contrib import admin
from .models import Category, Food, FoodVariant


admin.site.register(Category)


class FoodVariantInline(admin.TabularInline):
    model = FoodVariant
    extra = 1


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_available")
    inlines = [FoodVariantInline]