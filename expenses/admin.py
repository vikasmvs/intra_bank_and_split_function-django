from django.contrib import admin
from .models import Transaction, Balance, TemTransaction

# Register Transaction model
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('payer', 'recipient', 'amount', 'date', 'description')
    list_filter = ('payer', 'recipient', 'date')
    search_fields = ('payer__username', 'recipient__username')
    date_hierarchy = 'date'

# Register Balance model
@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    list_filter = ('user',)
    search_fields = ('user__username',)

# Register Transaction model
@admin.register(TemTransaction)
class TemTransactionAdmin(admin.ModelAdmin):
    list_display = ('payer', 'recipient', 'amount', 'date', 'description', 'temp_transaction_id', 'payers', 'status')
    list_filter = ('payer', 'recipient', 'date')
    search_fields = ('payer__username', 'recipient__username')
    date_hierarchy = 'date'

