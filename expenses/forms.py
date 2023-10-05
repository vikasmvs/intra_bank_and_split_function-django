from django import forms
from .models import Transaction, TemTransaction
from django.contrib.auth.models import User

class TransactionForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        fields = ('recipient', 'amount', 'description')
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)

class SplittingTransactionForm(forms.ModelForm):
    # Fields for the splitting transaction
    recipient = forms.ModelChoiceField(queryset=User.objects.all(), empty_label='Select a recipient')
    amount = forms.DecimalField(min_value=0.01)
    description = forms.CharField(max_length=255)

    # Field for selecting multiple payers
    payers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = TemTransaction
        fields = ['recipient', 'amount', 'description', 'payer', 'status', 'temp_transaction_id', 'payers', 'date']
