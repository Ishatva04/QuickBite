from django.shortcuts import render
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

