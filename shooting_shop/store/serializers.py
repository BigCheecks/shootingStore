from rest_framework import serializers
from .models import Category, Weapon, CartItem, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class WeaponSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Weapon
        fields = ['id', 'name', 'slug', 'description', 'price', 'stock', 'category']

class CartItemSerializer(serializers.ModelSerializer):
    weapon = WeaponSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'weapon', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'total_price', 'items']