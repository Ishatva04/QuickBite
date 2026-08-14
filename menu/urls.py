from django.urls import path
from . import views

urlpatterns = [
    path("", views.menu, name="menu"),
    path('<int:category_id>/', views.category_detail,name='category_detail'),
    path('food/<int:food_id>/',views.food_detail,name='food_detail'),
]