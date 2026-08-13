from django.shortcuts import render
from .models import Category

# Create your views here.

def menu(request):
    categories = Category.objects.all()
    return render(request,"menu.html",{"categories": categories})


def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    foods = category.food_set.all()
    return render(request,"category_detail.html",{"category": category, "foods": foods})