from django.contrib import admin
from .models import Order, Product, Category, Profile, ItemOrder

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ItemOrder)

