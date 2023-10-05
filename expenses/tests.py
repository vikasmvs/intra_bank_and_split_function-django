from django.test import TestCase
from django.contrib.auth.models import User
from .models import Transaction, Balance

class TransactionTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.transaction = Transaction.objects.create(
            payer=self.user1,
            recipient=self.user2,
            amount=100.00,
            date='2023-01-15',
            description='Test transaction'
        )

    def test_transaction_creation(self):
        transaction = Transaction.objects.get(id=self.transaction.id)
        self.assertEqual(transaction.payer, self.user1)
        self.assertEqual(transaction.recipient, self.user2)
        self.assertEqual(transaction.amount, 100.00)
        self.assertEqual(str(transaction.date), '2023-01-15')
        self.assertEqual(transaction.description, 'Test transaction')

class BalanceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.balance = Balance.objects.create(user=self.user, balance=500.00)

    def test_balance_creation(self):
        balance = Balance.objects.get(user=self.user)
        self.assertEqual(balance.user, self.user)
        self.assertEqual(balance.balance, 500.00)
