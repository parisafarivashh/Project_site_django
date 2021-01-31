from ..models import Product, Profile, Category, Order, ItemOrder
from ..views import OrderView, ItemOrderView, ProductsView, ProfileView, SignUpView
from django.test import RequestFactory, TestCase
from ..serializers import UserListSerializers, ProductSerializer, OrderSerializer
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
User = get_user_model()


class TestSerializer(TestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        # Every test needs access to the request factory.
        self.client = APIClient()
        self.user = User.objects.create_superuser(email='jacob@email.com', password='top_secret')

    def test_list_user(self):
        # Create an instance of a GET request.
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/users', follow=True)
        users = User.objects.all()
        serializer = UserListSerializers(users, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_list_product(self):
        game = Category.objects.create(name='game')
        Product.objects.create(name='ps4', price=1000000, stock=10, categories=game)
        Product.objects.create(name='ps5', price=1500000, stock=10, categories=game)
        Product.objects.create(name='ps1', price=500000,  stock=4, categories=game)

        response = self.client.get('/products', follow=True)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        # self.assertEqual(response.data, serializer.data)

    def test_list_order(self):
        user = User.objects.create_user(email='cob@email.com', password='to_secre')
        self.client.force_authenticate(user=user)
        Order.objects.create(user=user, paid=False)
        Order.objects.create(user=user, paid=True)
        response = self.client.get('/api/order/cart/') #return order wity pay false
        orders = Order.objects.filter(user=user).filter(paid=True)
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(response.data, serializer.data)




