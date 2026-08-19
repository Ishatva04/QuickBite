from django.urls import path
from . import views

urlpatterns = [
    path("table/<int:table_id>/",views.table_menu,name="table_menu"),
    path("checkout/", views.checkout, name="checkout"),
]