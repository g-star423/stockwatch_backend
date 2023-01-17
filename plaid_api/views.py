from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .serializers import UserTokenSerializer
from .models import UserToken
import json
from django.http import JsonResponse

# import environmental variables helper
import environ

env = environ.Env()
environ.Env.read_env()

# import requests
import requests


class UserTokenList(generics.ListCreateAPIView):
    queryset = UserToken.objects.all().order_by("id")
    serializer_class = UserTokenSerializer  # tell django what serializer to use


class UserTokenDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserToken.objects.all().order_by("id")
    serializer_class = UserTokenSerializer


def request_token(request):
    if request.method == "POST":
        print("made a post request")
        jsonRequest = json.loads(request.body)
        print(jsonRequest)

        plaid_request_body = {
            "client_id": env("CLIENT_ID"),
            "secret": env("SECRET_SANDBOX"),
            "client_name": "user" + str(jsonRequest["user_id"]),
            "country_codes": ["US"],
            "language": "en",
            "user": {"client_user_id": str(jsonRequest["user_id"])},
            "products": ["investments"],
        }

        # json_plaid_request_body = json.dumps(plaid_request_body)
        print(plaid_request_body)
        plaid_call = requests.post(
            "https://sandbox.plaid.com/link/token/create", json=plaid_request_body
        )
        # print(plaid_call.text)

        return JsonResponse(plaid_call.json())
