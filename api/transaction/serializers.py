from rest_framework import serializers
from .models import Account, Transaction

class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ('number', 'current_balance')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('retirante', 'receptora', 'method', 'qty', )
        ordering = ('created_at')