from django.utils import timezone

from accounts.models import CustomerProfile
from menu.models import Food
from management.models import Order


def quickbite_dashboard(request):

    if not request.path.startswith("/admin/"):
        return {}

    today = timezone.localdate()

    orders_today = Order.objects.filter(
        created_at__date=today
    ).count()

    preparing_orders = Order.objects.filter(
        status="preparing"
    ).count()

    available_foods = Food.objects.filter(
        is_available=True
    ).count()

    customers = CustomerProfile.objects.count()

    recent_orders = Order.objects.select_related(
        "user"
    ).order_by(
        "-created_at"
    )[:5]

    return {
        "qb_orders_today": orders_today,
        "qb_preparing_orders": preparing_orders,
        "qb_available_foods": available_foods,
        "qb_customers": customers,
        "qb_recent_orders": recent_orders,
    }