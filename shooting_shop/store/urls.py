from django.urls import include, path
from rest_framework import routers
from .views import CategoryViewSet, WeaponViewSet, CartItemViewSet, OrderViewSet, add_to_cart_view, cart_view, buy_view

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'weapons', WeaponViewSet, basename='weapon')
router.register(r'cart-items', CartItemViewSet, basename='cart-items')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
    path('add_to_cart/<int:weapon_id>/', add_to_cart_view, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('cart/buy/', buy_view, name='buy'),
]