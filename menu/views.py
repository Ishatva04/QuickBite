from django.shortcuts import render,get_object_or_404, redirect
from .models import Category,Food
from decimal import Decimal


# Create your views here.

def menu(request):
    categories = Category.objects.all()
    table_id = request.session.get("table_id")
    return render(request,"menu.html",{"categories": categories})


def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    foods = category.food_set.all()
    return render(request,"category_detail.html",{"category": category, "foods": foods})

def food_detail(request, food_id):
    food = Food.objects.get(id=food_id)
    return render(request,"food_detail.html", {"food": food})

def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")

def cart(request):
    
    cart = request.session.get("cart", {})

    items = []
    total = Decimal("0.00")

    for cart_key, quantity in cart.items():
        print("CART KEY:", cart_key)
        food_id, variant_id = cart_key.split("_")

        food = get_object_or_404(
            Food,
            id=food_id
        )

        variant = None

        if variant_id != "none":
            variant = get_object_or_404(
                food.variants,
                id=variant_id
            )

            price = variant.price

        else:
            price = food.price

        subtotal = price * quantity
        total += subtotal

        items.append({
            "food": food,
            "variant": variant,
            "quantity": quantity,
            "price": price,
            "subtotal": subtotal,
            "cart_key": cart_key,
        })

    return render(
        request,
        "cart.html",
        {
            "items": items,
            "total": total,
        }
    )



def add_to_cart(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    cart = request.session.get("cart", {})

    variant_id = request.POST.get("variant_id")

    if food.variants.exists():

        if not variant_id:
            return redirect("food_detail", food_id=food.id)

        variant = get_object_or_404(
            food.variants,
            id=variant_id,
            is_available=True
        )

        cart_key = f"{food.id}_{variant.id}"

    else:

        cart_key = f"{food.id}_none"

    if cart_key in cart:
        cart[cart_key] += 1
    else:
        cart[cart_key] = 1

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")

def increase_quantity(request, cart_key):
    cart = request.session.get("cart", {})

    cart_key = str(cart_key)

    if cart_key in cart:
        cart[cart_key] += 1

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def decrease_quantity(request, cart_key):
    cart = request.session.get("cart", {})

    cart_key = str(cart_key)

    if cart_key in cart:
        if cart[cart_key] > 1:
            cart[cart_key] -= 1
        else:
            del cart[cart_key]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def remove_from_cart(request, cart_key):
    cart = request.session.get("cart", {})

    cart_key = str(cart_key)

    if cart_key in cart:
        del cart[cart_key]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")
