from django.shortcuts import render, redirect, get_object_or_404
from .models import RestaurantTable, Order, OrderItem, Payment
from menu.models import Food
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
import razorpay
from django.http import JsonResponse,HttpResponse
from reportlab.pdfgen import canvas
from accounts.models import CustomerProfile
from .whatsapp import send_whatsapp_invoice


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

    for cart_key, quantity in cart.items():

        food_id, variant_id = cart_key.split("_")

        food = get_object_or_404(
            Food,
            id=food_id
        )

        variant = None

        if variant_id != "none":

            variant = get_object_or_404(
                food.variants,
                id=variant_id,
                is_available=True
            )

            price = variant.price

        else:

            price = food.price

        subtotal = price * quantity
        total += subtotal

        preparation_times.append(food.preparation_time)

        foods.append({
            "food": food,
            "variant": variant,
            "quantity": quantity,
            "price": price,
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
                variant=item["variant"],
                quantity=item["quantity"],
                price=item["price"],
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



def get_invoice_url(order, request):
    path = reverse(
        "invoice_pdf",
        args=[order.id]
    )

    return settings.PUBLIC_BASE_URL + (
        path + "?token=" + str(order.invoice_token)
    )



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

        profile = CustomerProfile.objects.filter(
            user=payment.order.user
        ).first()

        if profile and profile.phone_number:

            phone_number = "91" + profile.phone_number

            invoice_url = get_invoice_url(
                payment.order,
                request
            )

            whatsapp_response = send_whatsapp_invoice(
                phone_number,
                invoice_url,
                payment.order.user.first_name or payment.order.user.username,
                payment.order.id
            )

            print("INVOICE URL:", invoice_url)
            print("WHATSAPP STATUS:", whatsapp_response.status_code)
            print("WHATSAPP RESPONSE:", whatsapp_response.text)


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




def invoice(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    items = order.orderitem_set.all()

    return render(
        request,
        "invoice.html",
        {
            "order": order,
            "items": items,
        }
    )


def invoice_pdf(request, order_id):
    token = request.GET.get("token")
    order = get_object_or_404(
        Order,
        id=order_id,
        invoice_token=token
    )

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="invoice_{order.id}.pdf"'
    )

    pdf = canvas.Canvas(response)


    pdf.drawString(100, 800, "QuickBite Invoice")
    pdf.drawString(100, 760, f"Order ID: #{order.id}")
    pdf.drawString(100, 740, f"Customer: {order.user.username}")
    pdf.drawString(100, 720, f"Date: {order.created_at}")

    y = 680

    for item in order.orderitem_set.all():

        if item.variant:
            item_name = f"{item.variant.name}  {item.food.name}"
        else:
            item_name = item.food.name

        pdf.drawString(
            100,
            y,
            f"{item.food.name} | Qty: {item.quantity} | ₹{item.subtotal}"
        )
        y -= 30

    pdf.drawString(100, y - 20, f"Total: ₹{order.total}")
    pdf.drawString(100, y - 40, "Payment: Successful")

    pdf.save()

    return response