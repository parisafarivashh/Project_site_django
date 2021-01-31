from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate, APIClient, APIRequestFactory, APITestCase
from ..models import Order, ItemOrder, Product, Profile, Category
from ..views import ProductsView, SignUpView, ProfileView, OrderView, ItemOrderView, api_root, CategoryView
User = get_user_model()
PROFILE_URL = reverse('sign')


class ViewTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(email='user@email.com', password='secret')
        self.admin = User.objects.create_superuser(email='admin@email.com', password='admin')
        cloths = Category.objects.create(name='cloths')
        self.pants = Product.objects.create(name='pants',stock=2, price=30000,categories=cloths)
        order_1 = Order.objects.create(user=self.user, paid=False)
        order_2 = Order.objects.create(user=self.user, paid=True)

    def test_first_page(self):
        # Create an instance of a GET request.
        request = self.factory.get('')
        response = api_root(request)
        # Use this syntax for class-based views.
        self.assertEqual(response.status_code, 200)

    def test_signup(self):
        request = self.factory.post(PROFILE_URL, {"email": "jahan@email.com", "password": "top_secret"})
        response = SignUpView().as_view()(request)

        user = User.objects.get(email='jahan@email.com')
        order = user.orders.all()[0]
        self.assertEqual(order.paid, False)
        self.assertEqual(response.data, {"email": "jahan@email.com"})

    def test_list_category(self):
        # print(self.client)
        request = self.factory.get('api/category/')
        force_authenticate(request, user=self.user)
        response = CategoryView.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, 200)

    def test_create_category(self):
        request = self.factory.post('api/category/', {"name":"game"})
        force_authenticate(request, user=self.admin)
        response = CategoryView.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, {"name": "game"})

    def test_list_order(self):
        request = self.factory.get('api/order/')
        force_authenticate(request, user=self.user)
        response = OrderView.as_view({'get':'list'})(request)
        self.assertEqual(response.data[0]['user'],self.user.email)
        self.assertEqual(response.data[0]['paid'], False)
        self.assertEqual(response.status_code, 200)

    def test_list_product(self):
        request = self.factory.get('api/product/')
        product = Product.objects.all().values('name')
        response = ProductsView.as_view({'get':'list'})(request)
        self.assertEqual(response.data[0]['name'], product[0]['name'])
        self.assertEqual(response.status_code, 200)

    def test_create_product(self):
        request = self.factory.post('api/product/',{'name':'ps4', 'stock':2, 'price':30000, 'categories':1})
        force_authenticate(request, user=self.admin)
        response = ProductsView.as_view({'post':'create'})(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data,{'name': 'ps4', 'stock': 2, 'price': 30000.0, 'categories': 1})


class ListProductTest(APITestCase):

        def setUp(self):
            self.client = Client()

        def test_details(self):
            # self.assertTrue(self.client.login(username='user@email.com', password='1234'))
            print(User.objects.get_or_create(email='testuser@email.com')[0])
            self.client.force_login(User.objects.get_or_create(email='testuser@email.com')[0])
            response = self.client.get('/profile/', format='json')
            print(response.status_code)
            self.assertEqual(response.status_code, status.HTTP_200_OK)






























