from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import generics
from rest_framework.views import status
from rest_framework.response import Response
from rest_framework import permissions

from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from .utils import TransactionHelper
from .schema import TransactionViewSchema, AccountViewSchema


class ListCreateAccountsView(generics.ListCreateAPIView):
    """
    get:
    Return a list of all the existing accounts.

    post:
    Create a new account instance.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAdminUser, )
    schema = AccountViewSchema()

    def get(self, request, *args, **kwargs):
        return Response(AccountSerializer(self.queryset.all(), many=True).data)

    def post(self, request, *args, **kwargs):
        try:
            an_account = Account.objects.create(
                number=request.data.get('number'),
                current_balance=request.data.get('current_balance'),
                user=User.objects.create_user(
                    username=request.data.get('username'),
                    password=request.data.get('password'),
                ),
            )
            return Response(
                data=AccountSerializer(an_account).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as err:
            return Response(
                data={
                    'message': 'An exception happened: {}'.format(err)
                },
                status=status.HTTP_404_NOT_FOUND
            )
        

class AccountsDetailView(generics.RetrieveAPIView):
    """
    get:
    Return details the a existing account.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        try:
            an_account = self.queryset.get(pk=kwargs['pk'])
            return Response(AccountSerializer(an_account).data)
        except Account.DoesNotExist:
            return Response(
                data={
                    'message': 'Account with number: {} does not exist'.format(kwargs['pk'])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ListCreateTransactionView(generics.ListCreateAPIView):
    """
    get:
    Return a list of all the existing transactions.

    post:
    Create a new transaction instance.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    schema = TransactionViewSchema()

    def get(self, request, *args, **kwargs):
        try:
            current_user = request.user
            a_transaction = self.queryset.filter(
                Q(retirante=current_user) | Q(receptora=current_user)
            )
            return Response(TransactionSerializer(a_transaction, many=True).data)
        except Transaction.DoesNotExist:
            return Response(
                data={
                    "message": "Transaction with user_id: {} does not exist".format(request.user.id)
                },
                status=status.HTTP_404_NOT_FOUND
            )


    def post(self, request, *args, **kwargs):
        try:
            method = request.data.get('method')

            TRANS_TYPE = {
                'TDEP': 'TDEP',
                'TWD': 'TWD',
            }

            if method == TRANS_TYPE['TWD']:
                trans_ans = self.action_trans_withdraw(request)

            if method == TRANS_TYPE['TDEP']:
                trans_ans = self.action_trans_deposit(request)

            return Response(
                data=trans_ans['data'],
                status=status.HTTP_201_CREATED
            )

        except Exception as err:
            return Response(
                data={
                    'message': 'An exception happened: {}'.format(err)
                },
                status=status.HTTP_404_NOT_FOUND
            )

        
    def action_trans_withdraw(self, request):
        current_user = request.user
        qty = request.data.get('qty')
        method = request.data.get('method')

        data_trans_with = {
            "current_user": current_user,
            "method": method,
            "account": current_user,
            "qty": int(qty),
        }

        trans_helper = TransactionHelper()

        # verification account balance
        is_valid = trans_helper.checkout_balance(data_trans_with)

        if is_valid:

            # verification is withdraw possible
            money_ans = trans_helper.checkout_money(data_trans_with)
            # update current_balance 
            trans_helper.account_retirante_update(data_trans_with)
            # create transaction history
            trans_helper.transaction_insert(data_trans_with)

            return {
                'data': money_ans,
            }


    def action_trans_deposit(self, request):
        current_user = request.user
        account = request.data.get('account')
        qty = request.data.get('qty')
        method = request.data.get('method')

        trans_helper = TransactionHelper()

        # verification account exist
        account = trans_helper.checkout_account(account)

        if account:

            data_trans_dep = {
                "current_user": current_user,
                "method": method,
                "account": account,
                "qty": int(qty), 
            }
            
            # verification account balance
            is_valid = trans_helper.checkout_balance(data_trans_dep)

            if is_valid:
                # update balance current user
                trans_helper.account_retirante_update(data_trans_dep)
                # update balance receptor
                trans_helper.account_receptora_update(data_trans_dep)
                # create transaction history
                trans_ans = trans_helper.transaction_insert(data_trans_dep)

                return {
                    'data': TransactionSerializer(trans_ans).data
                }
