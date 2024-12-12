from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Weapon, CartItem, Order
from .serializers import CategorySerializer, WeaponSerializer, CartItemSerializer, OrderSerializer
from django.contrib.auth import login, logout
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required


def home_view(request):
    weapons = Weapon.objects.all()
    return render(request, 'index.html', {'weapons': weapons})

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def add_to_cart_view(request, weapon_id):
    weapon = get_object_or_404(Weapon, id=weapon_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, weapon=weapon)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def cart_view(request):
    if not request.user.is_authenticated:
        return render(request, 'not_logged_in.html', {
            'message': "Щоб переглянути кошик, вам необхідно увійти у свій акаунт."
        })
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def buy_view(request):
    if request.method == 'POST':
        CartItem.objects.filter(user=request.user).delete()
        return render(request, 'cart.html', {
            'cart_items': [],
            'purchase_message': "Всі гроші з вашої карти списано. Товар ви не отримаєте"
        })
    else:
        return redirect('cart')

def logout_view(request):
    logout(request)
    return redirect('home')

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class WeaponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializer
    permission_classes = [permissions.AllowAny]

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @action(methods=['post'], detail=False)
    def checkout(self, request):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total = sum(item.weapon.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=user, total_price=total)
        order.items.set(cart_items)
        cart_items.delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)