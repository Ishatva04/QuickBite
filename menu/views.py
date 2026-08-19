from django.shortcuts import render,get_object_or_404, redirect
from .models import Category,Food


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

    foods = []
    total = 0

    for food_id, quantity in cart.items():
        food = get_object_or_404(Food, id=food_id)

        subtotal = food.price * quantity
        total += subtotal

        foods.append({"food": food,"quantity": quantity,"subtotal": subtotal})

    return render(request,"cart.html",{"foods": foods,"total":total})



def add_to_cart(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    cart = request.session.get("cart", {})

    food_id = str(food.id)

    if food_id in cart:
        cart[food_id] += 1
    else:
        cart[food_id] = 1

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")

def increase_quantity(request, food_id):
    cart = request.session.get("cart", {})

    food_id = str(food_id)

    if food_id in cart:
        cart[food_id] += 1

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def decrease_quantity(request, food_id):
    cart = request.session.get("cart", {})

    food_id = str(food_id)

    if food_id in cart:
        if cart[food_id] > 1:
            cart[food_id] -= 1
        else:
            del cart[food_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def remove_from_cart(request, food_id):
    cart = request.session.get("cart", {})

    food_id = str(food_id)

    if food_id in cart:
        del cart[food_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")
