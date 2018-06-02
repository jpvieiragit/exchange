from rest_framework.schemas import AutoSchema
from coreapi import Field


class TransactionViewSchema(AutoSchema):
    """
    Overrides 'get_manual_fields()' to provide Custom Behavior X
    """

    def get_manual_fields(self, path, method):
        """Example adding per-method fields."""

        extra_fields = []
        if method=='POST':
            extra_fields = [
                Field('account', location="form", )
            ]

        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields
        

class AccountViewSchema(AutoSchema):
    """
    Overrides 'get_manual_fields()' to provide Custom Behavior X
    """

    def get_manual_fields(self, path, method):
        """Example adding per-method fields."""

        extra_fields = []
        if method=='POST':
            extra_fields = [
                Field('username', required=True, location="form", ),
                Field('password', required=True, location="form", )
            ]

        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields