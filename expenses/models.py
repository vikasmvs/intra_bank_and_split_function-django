from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    payer = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='transactions_paid')
    recipient = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='transactions_received')
    amount = models.DecimalField(max_digits=10, null=True, decimal_places=2)
    date = models.DateTimeField(null =True)
    description = models.TextField(null =True)

    def __str__(self):
        return f"Transaction #{self.id} ({self.amount} INR) from {self.payer} to {self.recipient}"

class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Balance for {self.user}"
    
class TemTransaction(models.Model):
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='temtransactions_paid')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='temtransactions_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    description = models.TextField()
    temp_transaction_id = models.TextField()
    payers = models.TextField()
    status = models.IntegerField(null =True)

    def __str__(self):
        return f"TemTransaction #{self.id} ({self.amount} INR) from {self.payer} to {self.recipient}"