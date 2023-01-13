from dataclasses import field
from rest_framework import serializers
from .models import Holding, TradeRequest


class HoldingSerializer(serializers.ModelSerializer):  # converting SQL data to JSON
    class Meta:
        model = Holding
        fields = (
            "id",
            "stock_name",
            "stock_ticker",
            "number_of_shares",
            "user_id",
        )


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeRequest
        fields = (
            "id",
            "stock_ticker",
            "number_of_shares",
            "stock_name",
            "trade_completed",
            "ticket_closed",
            "buying",
            "user_id",
        )
