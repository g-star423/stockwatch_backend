from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import HoldingSerializer, RequestSerializer
from .models import Holding, TradeRequest

# should handle getting ALL holdings - shouldn't use often
class HoldingList(generics.ListCreateAPIView):
    queryset = Holding.objects.all().order_by("id")
    serializer_class = HoldingSerializer


class HoldingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Holding.objects.all().order_by("id")
    serializer_class = HoldingSerializer


# handles getting all trades
class TradeList(generics.ListCreateAPIView):
    queryset = TradeRequest.objects.all().order_by("id")
    serializer_class = RequestSerializer


class TradeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TradeRequest.objects.all().order_by("id")
    serializer_class = RequestSerializer


class HoldingsByUser(generics.ListAPIView):
    serializer_class = HoldingSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Holding.objects.filter(user_id_id=user_id)
