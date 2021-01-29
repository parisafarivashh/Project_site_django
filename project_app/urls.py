from django.urls import path, include
from .views import SignUpView, UserList, CategoryView, ProductsView, ProfileView,\
    OrderView, ItemOrderView, api_root
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('category', CategoryView)
router.register('product', ProductsView)
router.register('order', OrderView, basename='orders')
router.register('item_order', ItemOrderView, basename='item_order')

urlpatterns = [
    path('sign/', SignUpView.as_view(), name='sign'),
    path('users/', UserList.as_view(),name='users'),
    path('api/', include(router.urls)),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('api-token-auth/', obtain_auth_token,name='api-token-auth'),
    path('', api_root)

]
