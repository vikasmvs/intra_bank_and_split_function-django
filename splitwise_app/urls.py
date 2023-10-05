from django.contrib import admin
from django.urls import path
from expenses import views as expense_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',expense_views.customer_login, name="index"),
    path('customer/dashboard/', expense_views.customer_dashboard, name='customer_dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('base.html', expense_views.base, name='base'),
    path('transaction/create/', expense_views.create_transaction, name='create_transaction'),
    path('balance/', expense_views.balance_list, name='balance_list'),
    path('expenses/transaction_list.html', expense_views.transaction_list, name='transaction_list'),
    path('expenses/transaction_created.html/<int:transaction_id>/', expense_views.transaction_created, name='transaction_created'),
    path('expenses/transaction_update.html/<int:transaction_id>/', expense_views.transaction_update, name='transaction_update'),
    path('expenses/transaction_delete.html/<int:transaction_id>/', expense_views.transaction_delete, name='transaction_delete'),
    path('splitting_transaction',expense_views.splitting_transaction, name="splitting_transaction"),
    path('tem_transaction_list',expense_views.tem_transaction_list, name="Split_Transactions_List"),
    path('temtransaction_approve/<int:transaction_id>/',expense_views.transaction_approve, name="temtransaction_approve"),
    path('temtransaction_deny/<int:transaction_id>/',expense_views.transaction_deny, name="temtransaction_deny")
]