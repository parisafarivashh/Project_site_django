from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Order, Category,  Profile, Product, ItemOrder
from django.contrib.auth import get_user_model
User = get_user_model()


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    cost = serializers.ReadOnlyField()
    # order_id = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'cost', 'paid']
        extra_kwargs = {'items': {'read_only': True}}

    def to_representation(self, instance):
        data = super(OrderSerializer, self).to_representation(instance)
        #print('date', data)
        lists = []
        for item in data['items']:
            id_product = ItemOrder.objects.filter(pk=item).values('product_id')
            count = ItemOrder.objects.filter(pk=item).values('count')
            lists.append((Product.objects.filter(pk=id_product[0]['product_id']).values(),count))

        data['items'] = lists

        return data


class ItemOrderSerializer(serializers.ModelSerializer):
    cost = serializers.ReadOnlyField()

    class Meta:
        model = ItemOrder
        fields = ['product', 'count','price', 'cost']
        extra_kwargs = {'price': {'read_only': True}}

    def to_representation(self, instance):
        data = super(ItemOrderSerializer, self).to_representation(instance)
        data['product'] = ProductSerializer(instance=instance.product).data
        data['order'] = OrderSerializer(instance=instance.order).data['id']
        # print(data)
        return data

    def create(self, validated_data):
        obj = ItemOrder.objects.create(**validated_data)
        return obj


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'colour', 'size', 'stock', 'price', 'categories']


class UserListSerializers(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(read_only=True, source='profile.address')

    class Meta:
        model = User
        fields = ['email', 'profile']


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    order_id = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = ['user', 'Country', 'city', 'street', 'number_apartment', 'order_id']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        token.save()
        profile = Profile.objects.create(user=user)
        profile.save()
        order = Order.objects.create(user=user)
        order.save()
        return user
