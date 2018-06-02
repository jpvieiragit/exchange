from .models import Account, Transaction

class TransactionHelper(object):

    def transaction_insert(self, data):
        a_transaction = Transaction(
            retirante=data["current_user"],
            receptora=data["account"],
            method=data["method"],
            qty=data["qty"]
        )
        a_transaction.save()
        return a_transaction


    def account_retirante_update(self, data):
        a_account = Account.objects.get(
            user=data["current_user"]
        )
        current_balance = a_account.current_balance - data["qty"]
        a_account.current_balance = current_balance
        a_account.save()
        return a_account


    def account_receptora_update(self, data):
        a_account = Account.objects.get(
            user=data["account"]
        )
        current_balance = a_account.current_balance + data["qty"]
        a_account.current_balance = current_balance
        a_account.save()
        return a_account


    def checkout_account(self, data):
        a_account = Account.objects.filter(number=data)
        if len(a_account) == 0:
            raise Exception("Account with number: {} does not exist".format(data))
        return a_account.get().user


    def checkout_balance(self, data):
        user_id = data["current_user"].id
        a_account = Account.objects.get(
            user_id=user_id
        )
        if data["qty"] > a_account.current_balance:
            raise Exception("Account with user_id: {} does not balance".format(user_id))
        return True


    def checkout_money(self, data):
        value = data["qty"]
        money_ans = {
            '100': 0,
            '50': 0,
            '20': 0,
            '10': 0,
            '5':0,
            '2':0,
        }

        qu = value//100
        value = value - (qu*100)
        money_ans['100'] = qu

        qu = value//50
        value = value - (qu*50)
        money_ans['50'] = qu

        qu = value//20
        value = value - (qu*20)
        money_ans['20'] = qu

        qu = value//10
        value = value - (qu*10)
        money_ans['10'] = qu

        qu = value//5
        value = value - (qu*5)
        money_ans['5'] = qu

        qu = value//2
        value = value - (qu*2)
        money_ans['2'] = qu

        if value > 0:
            raise Exception("Moneyless")

        return money_ans