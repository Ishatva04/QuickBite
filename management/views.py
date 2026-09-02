from django.shortcuts import render, redirect, get_object_or_404
from .models import RestaurantTable, Order, OrderItem, Payment
from menu.models import Food
from .models import RestaurantTable
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
import razorpay
from django.http import JsonResponse


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
    preparation_times = []

    for food_id, quantity in cart.items():

        food = get_object_or_404(Food, id=food_id)

        subtotal = food.price * quantity
        total += subtotal

        preparation_times.append(food.preparation_time)

        foods.append({
            "food": food,
            "quantity": quantity,
            "subtotal": subtotal
        })

    estimated_time = max(preparation_times)

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    if request.method == "POST":

        print("Place Order clicked")

        order = Order.objects.create(
            user=request.user,
            total=total,
            estimated_preparation_time=estimated_time
        )

        for item in foods:

            OrderItem.objects.create(
                order=order,
                food=item["food"],
                quantity=item["quantity"],
                price=item["food"].price,
                subtotal=item["subtotal"]
            )

        razorpay_order = client.order.create({
            "amount": int(total * 100),
            "currency": "INR",
            "payment_capture": 1
        })

        Payment.objects.create(
            order=order,
            razorpay_order_id=razorpay_order["id"]
        )

        return JsonResponse({
    "razorpay_order_id": razorpay_order["id"],
    "razorpay_key_id": settings.RAZORPAY_KEY_ID,
    "razorpay_amount": int(total * 100),
})

    return render(
        request,
        "checkout.html",
        {
            "foods": foods,
            "total": total,
        }
    )


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id,user=request.user)
    items = order.orderitem_set.all()
    statuses = ["pending","confirmed","preparing","ready","completed",]
    current_index = statuses.index(order.status)
    if order.preparing_started_at:
        expected_ready_time = (order.preparing_started_at + timedelta(minutes=order.estimated_preparation_time))
    else:
        expected_ready_time = None

    is_late = False

    if expected_ready_time:
        if timezone.now() > expected_ready_time:
            is_late = True
    return render(request,"confirmation.html",{"order": order,"items": items,"statuses": statuses,"current_index": current_index,"expected_ready_time": expected_ready_time,"is_late": is_late,})

def my_orders(request):

    if not request.user.is_authenticated:
        return redirect("login")

    orders = Order.objects.filter(user=request.user)

    return render(request,"my_orders.html",{"orders": orders})







def payment_verify(request):

    if request.method != "POST":
        return JsonResponse({
            "error": "Invalid request"
        }, status=400)

    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_signature = request.POST.get("razorpay_signature")

    payment = get_object_or_404(
        Payment,
        razorpay_order_id=razorpay_order_id,
        order__user=request.user
    )

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    try:

        client.utility.verify_payment_signature({
            "razorpay_order_id": payment.razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_signature": razorpay_signature
        })

        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.status = "successful"
        payment.save()

        payment.order.status = "confirmed"
        payment.order.save()

        request.session["cart"] = {}

        return JsonResponse({
            "success": True,
            "order_id": payment.order.id
        })

    except razorpay.errors.SignatureVerificationError:

        payment.status = "failed"
        payment.save()

        return JsonResponse({
            "success": False,
            "error": "Payment verification failed"
        }, status=400)


def payment_failed(request):

    if request.method != "POST":
        return JsonResponse({
            "error": "Invalid request"
        }, status=400)

    razorpay_order_id = request.POST.get("razorpay_order_id")

    payment = get_object_or_404(
        Payment,
        razorpay_order_id=razorpay_order_id,
        order__user=request.user
    )

    payment.status = "failed"
    payment.save()

    payment.order.status = "cancelled"
    payment.order.save()

    return JsonResponse({
        "success": True
    })