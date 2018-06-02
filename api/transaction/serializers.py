from rest_framework import serializers
from .models import Account, Transaction

class AccountSerializer(serializers.ModelSerializer):
	username = serializers.ReadOnlyField(source="user.username")

	class Meta:
		model = Account
		fields = ('number', 'current_balance', 'username')


class TransactionSerializer(serializers.ModelSerializer):
    retirante = serializers.ReadOnlyField(source="retirante.username")
    receptora = serializers.ReadOnlyField(source="receptora.username")

    class Meta:
        model = Transaction
        fields = ('method', 'qty', 'retirante', 'receptora')
        ordering = ('created_at')