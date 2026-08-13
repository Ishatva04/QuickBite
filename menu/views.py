from django.shortcuts import render
from .models import Category

# Create your views here.

def menu(request):
    categories = Category.objects.all()

    return render(
        request,
        "menu.html",
        {
            "categories": categories
        }
    )