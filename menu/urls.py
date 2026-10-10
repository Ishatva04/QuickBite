from django.urls import path
from . import views
from menu import views

urlpatterns = [
    path("", views.menu, name="menu"),
    path('<int:category_id>/', views.category_detail,name='category_detail'),
    path('food/<int:food_id>/',views.food_detail,name='food_detail'),
    path('cart/',views.cart,name='cart'),
    path('cart/add/<int:food_id>/',views.add_to_cart,name="add_to_cart"),
    path("increase/<str:cart_key>/",views.increase_quantity,name="increase_quantity"),
    path("decrease/<str:cart_key>/",views.decrease_quantity,name="decrease_quantity"),
    path("remove/<str:cart_key>/",views.remove_from_cart,name="remove_from_cart"),
]