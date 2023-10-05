from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Transaction, Balance, TemTransaction
from .forms import TransactionForm, SplittingTransactionForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone


def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('customer_dashboard')
            else:
                messages.error(request, 'Your account is not active.')
        else:
            messages.error(request, 'Invalid login credentials.')
    return render(request, 'expenses/customer_login.html')


@login_required
def customer_dashboard(request):
    pending_transactions = TemTransaction.objects.filter(Q(payers=request.user) , status = None )
    deny_transactions = TemTransaction.objects.filter(Q(payers=request.user) , status = 0 )
    approved_transactions = TemTransaction.objects.filter(Q(payers=request.user) , status = 1)
    context = {'approved_transactions': approved_transactions , 'deny_transactions': deny_transactions , 'pending_transactions': pending_transactions }
    return render(request, 'expenses/customer_dashboard.html', context)

@login_required
def create_transaction(request):
    user_balances = Balance.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = TransactionForm(request.POST, current_user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.payer = request.user
            if transaction.amount <= user_balances.balance :
                user_balances.balance -= transaction.amount
                user_balances.save(update_fields=["balance"])
                recipient_balance = Balance.objects.get(user=transaction.recipient)
                recipient_balance.balance += transaction.amount
                transaction.date = timezone.now()
                recipient_balance.save(update_fields=["balance"])
                transaction.save()
                messages.success(request, 'Transaction created successfully.')
                return redirect('transaction_created', transaction_id=transaction.id)
            else:
                messages.error(request, 'Insufficient balance to create the transaction.')
    else:
        form = TransactionForm(current_user=request.user)
    context = {'balances': user_balances, 'form': form}
    return render(request, 'expenses/create_transaction.html', context)

@login_required
def balance_list(request):
    user_balances = Balance.objects.filter(user=request.user)
    context = {'balances': user_balances}
    return render(request, 'expenses/balance_list.html', context)

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(Q(payer=None) | Q(payer=request.user) | Q(recipient=request.user) )
    context = {'transactions': transactions}
    return render(request, "expenses/transaction_list.html", context)

@login_required
def tem_transaction_list(request):
    TemTransaction_2 = TemTransaction.objects.filter(Q(payer=request.user) | Q(recipient=request.user) | Q(payers__contains=request.user.username ))
    context = {'transactions': TemTransaction_2 }
    return render(request, "expenses/temtransaction_list.html", context)

@login_required
def transaction_approve(request, transaction_id):
    transaction = get_object_or_404(TemTransaction, id=transaction_id)

    if not (request.user == transaction.payer or request.user or transaction.payers_contains == transaction.recipient):
        messages.error(request, 'You do not have permission to Approve this transaction.')
        return redirect('Split_Transactions_List')
    
    if request.method == 'POST':
        user_balances = Balance.objects.filter(user=request.user).first()
        recipient_balance = Balance.objects.get(user=transaction.recipient)
        if transaction.amount <= user_balances.balance :
            user_balances.balance -= transaction.amount
            user_balances.save(update_fields=["balance"])
            recipient_balance.balance += transaction.amount
            recipient_balance.save(update_fields=["balance"])
            transaction.save()
            messages.success(request, 'Transaction created successfully.')
            transaction.status = 1
            transaction.save()
        else:
            messages.error(request, 'Insufficient balance to create the transaction.')
            return redirect('Split_Transactions_List')

        messages.success(request, 'Approved')
        return redirect('Split_Transactions_List')

    return render(request, "expenses/temtransaction_approve.html")


@login_required
def transaction_deny(request, transaction_id):
    transaction = get_object_or_404(TemTransaction, id=transaction_id)

    if not (request.user == transaction.payer or request.user or transaction.payesr_contains == transaction.recipient):
        messages.error(request, 'You do not have permission to deny this transaction.')
        return redirect('transaction_list')

    if request.method == 'POST':
        transaction.status = 0
        transaction.save()
        #\transaction.delete()
        messages.error(request, 'Denyed.')
        return redirect('Split_Transactions_List')
    
    return render(request,"expenses/temtransaction_deny.html")


@login_required
def base(request):
    user_balance = None
    if request.user.is_authenticated:
        user_balance = Balance.objects.get(user=request.user)
    context = {'user_balance': user_balance}
    print(context)
    return render(request,"base.html", context)


@login_required
def transaction_created(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    return render(request, 'expenses/transaction_created.html', {'transaction': transaction})


@login_required
def transaction_delete(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully.')
        return redirect('transaction_list')

    return render(request, 'expenses/transaction_delete.html')


@login_required
def transaction_update(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if not (request.user == transaction.payer or request.user == transaction.recipient):
        messages.error(request, 'You do not have permission to edit this transaction.')
        return redirect('transaction_list')

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully.')
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)

    context = {'form': form}
    return render(request, 'expenses/transaction_update.html', context)

@login_required
def splitting_transaction(request):
    if request.method == 'POST':
        form = SplittingTransactionForm(request.POST)
        print(form.is_valid())
        if request.POST:
            recipient = form.cleaned_data['recipient']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            payers = form.cleaned_data['payers']
            payer=request.user
            temp_transaction_id = Transaction(description=form.cleaned_data['description'])
            temp_transaction_id.save()

            split_amount = amount / len(payers)

            for payer in payers:
                if payer  == request.user:
                    user_balances = Balance.objects.filter(user=request.user).first()
                    recipient_balance = Balance.objects.get(user=recipient)
                    if split_amount <= user_balances.balance :
                        user_balances.balance -= split_amount
                        user_balances.save(update_fields=["balance"])
                        recipient_balance.balance += split_amount
                        recipient_balance.save(update_fields=["balance"])
                        transaction.save()
                        messages.success(request, 'Transaction created successfully.')
                        status_of_user = 1
                    else:
                        messages.error(request, 'Insufficient balance to create the transaction.')
                        return redirect('Split_Transactions_List')
                else:
                    status_of_user = None
                transaction = TemTransaction(
                    recipient=recipient,
                    payers=payer.username,
                    amount=split_amount,
                    description=description,
                    temp_transaction_id=temp_transaction_id.id,
                    date=timezone.now(),
                    payer=request.user,
                    status=status_of_user
                )
                transaction.save()
                
            messages.success(request, 'Split transaction created successfully.')
            return redirect('Split_Transactions_List')

    else:
        form = SplittingTransactionForm()

    users = User.objects.exclude(id=request.user.id)
    current_user_id = request.user.id
    context = {'form': form, 'users': users, 'current_user_id': current_user_id}
    return render(request, 'expenses/splitting_transaction.html', context)