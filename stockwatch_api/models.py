from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class Holding(models.Model):
    stock_name = models.CharField(max_length=255)
    stock_ticker = models.CharField(max_length=9)
    number_of_shares = models.DecimalField(max_digits=8, decimal_places=2)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)


class TradeRequest(models.Model):
    stock_ticker = models.CharField(max_length=9)
    number_of_shares = models.DecimalField(max_digits=8, decimal_places=2)
    stock_name = models.CharField(max_length=255)
    trade_completed = models.BooleanField()
    ticket_closed = models.BooleanField()
    buying = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
