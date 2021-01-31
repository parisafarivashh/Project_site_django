from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Product, Profile, Category, Order, ItemOrder
from django.test import Client
from django.contrib.auth import get_user_model
User = get_user_model()


class TestCategory(TestCase):
    def setUp(self):
        Category.objects.create(name='game')

    def test_create_category(self):
        category1 = Category.objects.get(name='game')
        self.assertEqual(category1.name, "game")


class TestProduct(TestCase):
    def setUp(self):
        game = Category.objects.create(name='game')
        Product.objects.create(name='ps4', stock=10, price=1000000, categories=game)

    def test_create_product(self):
        product = Product.objects.get(name='ps4')
        game = Category.objects.get(name='game')
        self.assertEqual(product.name, "ps4")
        self.assertEqual(product.stock, 10)
        self.assertEqual(product.categories, game)


class TestOrder(TestCase):
    def setUp(self):
        saba = User.objects.create_user(email='saba@email.com', password='saba123')
        Order.objects.create(user=saba, paid=False)

    def test_create_order(self):
        id_user = User.objects.get(email='saba@email.com')
        order_1 = Order.objects.get(user=id_user.id)
        self.assertEqual(order_1.user.id, id_user.id)


class TestItemOrder(TestCase):
    def setUp(self):
        saimin = get_user_model().objects.create_user(email='saimin@email.com', password='saimin123')
        order = Order.objects.create(user=saimin, paid=False)
        game = Category.objects.create(name='game')
        ps4 = Product.objects.create(name='ps4', stock=10, price=1000000, categories=game)
        ItemOrder.objects.create(price=1000000, product=ps4, order=order, count=2)

    def test_create_item(self):
        ps4 = Product.objects.get(name='ps4')
        item = ItemOrder.objects.get(product=ps4)
        self.assertEqual(item.cost, 2000000)
        self.assertEqual(item.count, 2)





