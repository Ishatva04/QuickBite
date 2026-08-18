from django.urls import path
from . import views
from menu import views

urlpatterns = [
    path("", views.menu, name="menu"),
    path('<int:category_id>/', views.category_detail,name='category_detail'),
    path('food/<int:food_id>/',views.food_detail,name='food_detail'),
    path('cart/',views.cart,name='cart'),
    path('cart/add/<int:food_id>/',views.add_to_cart,name="add_to_cart"),
    path("increase/<int:food_id>/",views.increase_quantity,name="increase_quantity"),
    path("decrease/<int:food_id>/",views.decrease_quantity,name="decrease_quantity"),
    path("remove/<int:food_id>/",views.remove_from_cart,name="remove_from_cart"),
]