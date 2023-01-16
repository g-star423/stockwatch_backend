from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import UserTokenSerializer
from .models import UserToken


class UserTokenList(generics.ListCreateAPIView):
    queryset = UserToken.objects.all().order_by("id")
    serializer_class = UserTokenSerializer  # tell django what serializer to use


class UserTokenDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserToken.objects.all().order_by("id")
    serializer_class = UserTokenSerializer
