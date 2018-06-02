from rest_framework import serializers
from .models import Account, Transaction

class AccountSerializer(serializers.ModelSerializer):
	username = serializers.ReadOnlyField(source="user.username")

	class Meta:
		model = Account
		fields = ('number', 'current_balance', 'username')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('method', 'qty')
        ordering = ('created_at')