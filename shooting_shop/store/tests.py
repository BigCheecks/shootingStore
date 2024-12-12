from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Weapon, CartItem

class StoreTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.category = Category.objects.create(name="Пістолети", slug="pistols")
        self.weapon = Weapon.objects.create(
            category=self.category,
            name="Beretta M9",
            slug="beretta-m9",
            description="Тестовий пістолет",
            price=1000,
            stock=10
        )

        self.home_url = reverse('home')
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.cart_url = reverse('cart')
        self.add_to_cart_url = reverse('add_to_cart', args=[self.weapon.id])
        self.buy_url = reverse('buy')

    def test_home_page_status_code(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Наші товари")

    def test_registration(self):
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'Newuser123',
            'password2': 'Newuser123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        user = User.objects.get(username='testuser')
        self.assertTrue(user.is_authenticated)

    def test_cart_view_not_logged_in(self):
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Щоб переглянути кошик, вам необхідно увійти")

    def test_add_to_cart_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(self.add_to_cart_url)
        self.assertEqual(response.status_code, 302)
        cart_item_exists = CartItem.objects.filter(user=self.user, weapon=self.weapon).exists()
        self.assertTrue(cart_item_exists)

    def test_cart_view_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        self.client.get(self.add_to_cart_url)
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.weapon.name)
        self.assertContains(response, "Купити")

    def test_buy_view(self):
        self.client.login(username='testuser', password='testpass')
        self.client.get(self.add_to_cart_url)
        response = self.client.post(self.buy_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "всі гроші з вашої карти списано. товар ви не отримаєте")
        cart_items = CartItem.objects.filter(user=self.user)
        self.assertEqual(cart_items.count(), 0)