from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate

def signup(request):
    error = None
    next_url = request.GET.get("next")

    if request.method == "POST":
        username = request.POST.get("username")
        next_url = request.POST.get("next")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if not username:
            error = "Username is required"

        elif password != confirm_password:
            error = "Passwords do not match"

        elif User.objects.filter(username=username).exists():
            error = "Username already exists"

        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            if next_url:
                return redirect(f"/accounts/login/?next={next_url}")

            return redirect("login")

    return render(request,"signup.html",{"error": error,"next": next_url}
)

def login_view(request):
    error = None
    next_url = request.GET.get("next")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next")

        user = authenticate(
            username=username,
            password=password
        )
        if user is None:
            error = "Invalid username or password"
        else:
            login(request, user)

            if next_url:
                return redirect(next_url)
            
            return redirect("home")

    return render(request,"login.html",{"error": error, "next": next_url,})

def logout_view(request):
    logout(request)
    return redirect("home")

