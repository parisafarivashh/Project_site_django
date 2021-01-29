from django.shortcuts import render
from rest_framework.decorators import action, api_view
from django.http import Http404
from django.shortcuts import render
from django.db import transaction
from rest_framework import generics, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.reverse import reverse
from .serializers import SignUpSerializer, UserListSerializers, CategorySerializer, \
    ProductSerializer, ProfileSerializer, OrderSerializer, ItemOrderSerializer
from .permissions import IsAdmin, IsOwn, UserPermissions
from .models import Profile, Product, Category, Order, ItemOrder
from django.contrib.auth import get_user_model

User = get_user_model()
@api_view(['GET'])
def api_root(request):
    return Response({
        'sign': reverse('sign', request=request),
        'profile': reverse('profile', request=request),
        'users': reverse('users', request=request),

    })


class ItemOrderView(viewsets.mixins.CreateModelMixin,
                    viewsets.mixins.UpdateModelMixin,
                    viewsets.mixins.DestroyModelMixin,
                    viewsets.mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = ItemOrderSerializer
    queryset = ItemOrder.objects.all()

    def perform_create(self, serializer):
        serializer.save(order=self.request.user.last_order)


class OrderView(viewsets.mixins.ListModelMixin,
                viewsets.mixins.DestroyModelMixin,
                viewsets.mixins.RetrieveModelMixin,
                viewsets.mixins.UpdateModelMixin,
                viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated, IsOwn)
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user.is_staff
        if user==True:
            return Order.objects.all().filter(paid=False)
        else:
            user = self.request.user
            return Order.objects.filter(user=user).filter(paid=False)

    @action(detail=True, url_path='paid', methods=['get'])
    def paid(self, request, *args, **kwargs):
        user = self.get_object()
        order_id = kwargs['pk']
        with transaction.atomic():
            order = Order.objects.get(id=order_id)
            order.paid = True
            order.save()
            order = Order.objects.create(user=self.request.user)
            order.save()
            if len(Order.objects.filter(paid=False).filter(user=self.request.user))> 1:
                order.delete()

            return Response(status=status.HTTP_200_OK)

    @action(detail=False, url_path='cart', methods=['get'])
    def cart(self, request, *args, **kwargs):
        user = self.request.user
        cart = Order.objects.filter(user=user).filter(paid=True)
        serializer = self.get_serializer(cart, many=True)
        return Response(serializer.data)


class CategoryView(viewsets.ModelViewSet):
    permission_classes = (UserPermissions,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class UserList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,IsAdmin,)
    serializer_class = UserListSerializers
    queryset = User.objects.all()


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProductsView(viewsets.ModelViewSet):
    permission_classes = (UserPermissions,)
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    # def get_permissions(self):
    #     Your logic should be all here
    #     if self.action in ('create', 'update', 'destroy'):
    #         self.permission_classes = (UserPermissions, IsAuthenticated,)
    #     return super(self.__class__, self).get_permissions()


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwn,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Profile.objects.filter(user=user)
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj
