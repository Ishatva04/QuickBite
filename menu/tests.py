from django.test import TestCase
from .models import Category, Food, FoodVariant


class FoodVariantTest(TestCase):

    def test_variant_price(self):
        category = Category.objects.create(
            name="Pizza",
            description="Our delicious pizzas"
        )

        pizza = Food.objects.create(
            category=category,
            name="Pizza",
            price=300
        )

        variant = FoodVariant.objects.create(
            food=pizza,
            name="Medium",
            price=300
        )

        self.assertEqual(variant.price, 250)