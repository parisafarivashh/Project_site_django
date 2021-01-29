from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import transaction
from django.shortcuts import Http404


class UserProfileManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('user must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def last_order(self):
        return self.orders.all().filter(paid=False).last()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, unique=True)
    colour = models.CharField(max_length=100, unique=True)
    size = models.CharField(max_length=100, unique=True)
    stock = models.IntegerField()
    price = models.FloatField()
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)

    @property
    def cost(self):
        """
        self is object order
        """
        cost = 0
        for item in self.items.all():
            cost += item.cost
        return cost

    def delete(self, using=None, keep_parents=False, *args, **kwargs):
        with transaction.atomic():
            for item in self.items.all():
                print('itemm',item)
                # super(ItemOrder, item).delete(item)
                item.delete()
            print('self',self)
            super(Order, self).delete(*args, **kwargs)


class ItemOrderManager(models.Manager):

    def create(self, **kwargs):
        #print(self.request.user)
        print('sellllf',self)
        print(kwargs)
        product = kwargs.get('product', None)
        order = kwargs.get('order', None)
        count = kwargs.get('count', None)
        price = product.price

        id_product = Product.objects.all().filter(name=product).values('id')[0]['id']

        with transaction.atomic():
            product.stock -= count
            if product.stock < 0:
                raise Http404
            product.save()

            instance = order.items.filter(product_id=id_product)
            if instance:
                Total_count = instance[0].count + count
                instance[0].count = Total_count
                instance[0].save()

                return instance[0]
            else:
                instance = super().create(price=price, product=product, order=order, count=count)
                return instance


class ItemOrder(models.Model):
    price = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    count = models.IntegerField()

    objects = ItemOrderManager()

    @property
    def cost(self):
        return self.price * self.count

    def delete(self, using=None, keep_parents=False,*args, **kwargs):
        print('selfee 2',self)#ItemOrder object 3
        # instance = Product.objects.filter(name=self.product)[0]
        # instance.stock +=self.count
        # instance.save()
        print(self.product.stock)
        super(ItemOrder, self).delete(*args, **kwargs)
        self.product.stock += self.count
        print(self.product.stock)
        self.product.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Country = models.CharField(max_length=200,null=True)
    City = models.CharField(max_length=200, null=True)
    street = models.CharField(max_length=200, null=True)
    number_apartment = models.IntegerField()

    def __unicode__(self):
        return self.user.email

    @property
    def order_id(self):
        data = self.user.orders.filter(paid=True).last()
        return data.id



