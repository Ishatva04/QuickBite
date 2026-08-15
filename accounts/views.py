from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login


def signup(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            error = "Passwords do not match"

        elif User.objects.filter(username=username).exists():
            error = "Username already exists"

        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

    return render(request,"signup.html",{"error": error}
)

def login_view(request):
    return render(request,'login.html')