from django.urls import path
from . import views

urlpatterns = [
    path("table/<int:table_id>/", views.table_menu, name="table_menu"),
    path("checkout/", views.checkout, name="checkout"),
    path("payment/verify/", views.payment_verify, name="payment_verify"),
    path("payment/failed/",views.payment_failed,name="payment_failed"),
    path("order/<int:order_id>/", views.order_confirmation, name="order_confirmation"),
    path("orders/", views.my_orders, name="my_orders"),
    path("invoice/<int:order_id>/", views.invoice, name= "invoice"),
    path("invoice/<int:order_id>/pdf/", views.invoice_pdf,name = "invoice_pdf"),
]