from django.shortcuts import get_object_or_404, redirect

from .models import RestaurantTable


def table_menu(request, table_id):
    table = get_object_or_404(
        RestaurantTable,
        id=table_id,
        is_active=True
    )
    request.session["table_id"] = table.id
    return redirect("menu")