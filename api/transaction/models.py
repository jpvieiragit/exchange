from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=5, primary_key=True)
    current_balance = models.IntegerField(default=0)

    def __str__(self):
        return "Account number - {}".format(self.number)


class Transaction(models.Model):
	CHOICES = (
        ('TWD', 'Withdraw'),
        ('TDEP', 'Deposit'),
    )
    
	retirante = models.IntegerField()
	receptora = models.IntegerField()
	method = models.CharField(max_length=4, choices=CHOICES)
	qty = models.IntegerField(default=0)
	created_at = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return "{} - ${}".format(self.method, self.qty)



