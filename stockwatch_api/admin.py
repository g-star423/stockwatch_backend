from django.contrib import admin

# Register your models here.
from .models import Holding
from .models import TradeRequest

admin.site.register(Holding)
admin.site.register(TradeRequest)
