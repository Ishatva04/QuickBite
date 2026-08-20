from django.contrib import admin
from .models import RestaurantTable,Order,OrderItem

# Register your models here.
admin.site.register(RestaurantTable)
admin.site.register(Order)
admin.site.register(OrderItem)