from django.shortcuts import render, redirect, get_object_or_404
from .models import RestaurantTable, Order, OrderItem
from menu.models import Food
from .models import RestaurantTable
from django.urls import reverse


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
        login_url = reverse("login")
        return redirect(f"{login_url}?next=/management/checkout/")
    

    foods = []
    total = 0
    for food_id, quantity in cart.items():
        food = get_object_or_404(Food, id=food_id)

        subtotal = food.price * quantity
        total += subtotal

        foods.append({
            "food": food,
            "quantity": quantity,
            "subtotal": subtotal
        })
    if request.method == "POST":
        print("Place Order clicked")
        order = Order.objects.create(
            user=request.user,
            total=total
        )
        for item in foods:
            OrderItem.objects.create(
                order=order,
                food=item["food"],
                quantity=item["quantity"],
                price=item["food"].price,
                subtotal=item["subtotal"]
            )
        request.session["cart"] = {}
        return redirect("order_confirmation",order_id=order.id)
    return render(request,"checkout.html",{"foods": foods,"total": total})


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.orderitem_set.all()
    return render(request,"confirmation.html",{"order": order,"items": items})