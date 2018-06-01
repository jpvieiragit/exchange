from django.urls import path
from .views import ListCreateTransactionView, ListCreateAccountsView, AccountsDetailView


urlpatterns = [
    path('transactions/', ListCreateTransactionView.as_view(), name="transactions-list-create"),
    path('accounts/', ListCreateAccountsView.as_view(), name="accounts-list-create"),
    path('accounts/<pk>/', AccountsDetailView.as_view(), name="accounts-detail"),
]