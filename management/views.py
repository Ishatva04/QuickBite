from django.shortcuts import render, redirect, get_object_or_404
from .models import RestaurantTable, Order, OrderItem
from menu.models import Food
from .models import RestaurantTable


def table_menu(request, table_id):
    table = get_object_or_404(
        RestaurantTable,
        id=table_id,
        is_active=True
    )
    request.session["table_id"] = table.id
    return redirect("menu")

def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("cart")

    if not request.user.is_authenticated:
        return redirect("login")