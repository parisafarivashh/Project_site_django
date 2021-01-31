from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from ..permissions import IsAdmin, IsOwn
from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
User = get_user_model()


class TestPermission(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin = User.objects.create_superuser(email='admin@gmail.com',password='admin997')
        self.user = User.objects.create_user(email='user@gmail.com', password='user')

    def test_admin_permission(self):

        request = self.factory.get('/users')
        request.user = self.admin
        permission = IsAdmin()
        has_permission = permission.has_permission(request, None)
        self.assertTrue(has_permission)

    def test_own_permission(self):
        request = self.factory.get('/api/order/cart')
        force_authenticate(request, user=self.user)
        request.user = self.user
        permission = IsOwn()
        has_permissin = permission.has_permission(request, None)
        self.assertTrue(has_permissin)





