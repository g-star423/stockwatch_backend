from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from stockwatch_api.models import Holding
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

# to allow database manipulation
from django.db import connection

# importing model
from . import models


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


def exchange_token(request):
    if request.method == "POST":
        jsonRequest = json.loads(request.body)

        user_id = jsonRequest["user_id"]

        plaid_exchange_request_body = {
            "client_id": env("CLIENT_ID"),
            "secret": env("SECRET_SANDBOX"),
            "public_token": jsonRequest["public_token"],
        }

        exchange_call = requests.post(
            "https://sandbox.plaid.com/item/public_token/exchange",
            json=plaid_exchange_request_body,
        )
        exchange_call_json = exchange_call.json()
        private_key = exchange_call_json["access_token"]
        # conn = psycopg2.connect("stockwatch_api") used different code - can delete later
        cur = connection.cursor()
        cur.execute(
            f"INSERT INTO plaid_api_usertoken (link_token, token_status, user_id_id) VALUES ('{private_key}', 'back from plaid OK', (SELECT id FROM auth_api_useraccount WHERE id={user_id}))"
        )
        # conn.commit() -- can delete later
        # cur.close()
        # conn.close()
        return JsonResponse({"response": "hopefully ok"})


def update_holdings(request):
    if request.method == "POST":
        jsonRequest = json.loads(request.body)
        user_id = jsonRequest["user_id"]
        # cur = connection.cursor()
        # cur.execute(
        #     f"SELECT link_token FROM plaid_api_usertoken WHERE user_id_id={user_id}"
        # )
        # access_token = cur.fetchone()
        # print("start access token")
        # print(access_token)
        # print("finish access token")

        # holdings_request_body = {
        #     "client_id": env("CLIENT_ID"),
        #     "secret": env("SECRET_SANDBOX"),
        #     "access_token": access_token[0],
        # }
        # holdings = requests.post(
        #     "https://sandbox.plaid.com/investments/holdings/get",
        #     json=holdings_request_body,
        # )
        # holdingsJson = holdings.json()
        # print(holdingsJson)

        data = {
            "accounts": [
                {
                    "account_id": "dngqEJPWQ8slrAEdE191tPJDkEqy7ecDgRrje",
                    "balances": {
                        "available": 100,
                        "current": 110,
                        "iso_currency_code": "USD",
                        "limit": None,
                        "unofficial_currency_code": None,
                    },
                    "mask": "0000",
                    "name": "Plaid Checking",
                    "official_name": "Plaid Gold Standard 0% Interest Checking",
                    "subtype": "checking",
                    "type": "depository",
                },
                {
                    "account_id": "aWkwp3agj9udLXlZl1g1cWw13ZP8gEu1dDVBQ",
                    "balances": {
                        "available": 200,
                        "current": 210,
                        "iso_currency_code": "USD",
                        "limit": None,
                        "unofficial_currency_code": None,
                    },
                    "mask": "1111",
                    "name": "Plaid Saving",
                    "official_name": "Plaid Silver Standard 0.1% Interest Saving",
                    "subtype": "savings",
                    "type": "depository",
                },
                {
                    "account_id": "4e6XLVQ7lGIoPVGkG4K4IzLB4DK7o3FnDL4QM",
                    "balances": {
                        "available": None,
                        "current": 1000,
                        "iso_currency_code": "USD",
                        "limit": None,
                        "unofficial_currency_code": None,
                    },
                    "mask": "2222",
                    "name": "Plaid CD",
                    "official_name": "Plaid Bronze Standard 0.2% Interest CD",
                    "subtype": "cd",
                    "type": "depository",
                },
                {
                    "account_id": "NxqpKnQzWgHzpQnMnXJXU4REGQnDWxFneQk4Q",
                    "balances": {
                        "available": None,
                        "current": 410,
                        "iso_currency_code": "USD",
                        "limit": 2000,
                        "unofficial_currency_code": None,
                    },
                    "mask": "3333",
                    "name": "Plaid Credit Card",
                    "official_name": "Plaid Diamond 12.5% APR Interest Credit Card",
                    "subtype": "credit card",
                    "type": "credit",
                },
                {
                    "account_id": "PargzEM3Goh3g4eZezmzUPQRxEKjMwcQ3AVPy",
                    "balances": {
                        "available": 43200,
                        "current": 43200,
                        "iso_currency_code": "USD",
                        "limit": None,
                        "unofficial_currency_code": None,
                    },
                    "mask": "4444",
                    "name": "Plaid Money Market",
                    "official_name": "Plaid Platinum Standard 1.85% Interest Money Market",
                    "subtype": "money market",
                    "type": "depository",
                },
                {
                    "account_id": "jqpxEgMyoPH7qEdkdLnLIWRZkoNP1buZpalVK",
                    "balances": {
                        "available": None,
                        "current": 320.76,
                        "iso_currency_code": "USD",
                        "limit": None,
                        "unofficial_currency_code": None,
                    },
                    "mask": "5555",
                    "name": "Plaid IRA",
                    "official_name": None,
                    "subtype": "ira",
                    "type": "investment",
                },
                {
                    "account_id": "7MPwqV1ZrlUAq35b5VnVHxKmG64REpiMvxroy",
                    "balances": {
                        "available": None,
                        "current": 23631.9805,
                        "iso_currency_code": "USD",
                        "limit": None,
                        "unofficial_currency_code": None,
                    },
                    "mask": "6666",
                    "name": "Plaid 401k",
                    "official_name": None,
                    "subtype": "401k",
                    "type": "investment",
                },
                {
                    "account_id": "ek6KEJjAZ1fPWenQnzDzhXM7o9kDeau76me49",
                    "balances": {
                        "available": None,
                        "current": 65262,
                        "iso_currency_code": "USD",
                        "limit": None,
                        "unofficial_currency_code": None,
                    },
                    "mask": "7777",
                    "name": "Plaid Student Loan",
                    "official_name": None,
                    "subtype": "student",
                    "type": "loan",
                },
                {
                    "account_id": "Q4z8BW1xnmhxWKgZgo6oSjmvyQrdLnF3yDR5Q",
                    "balances": {
                        "available": None,
                        "current": 56302.06,
                        "iso_currency_code": "USD",
                        "limit": None,
                        "unofficial_currency_code": None,
                    },
                    "mask": "8888",
                    "name": "Plaid Mortgage",
                    "official_name": None,
                    "subtype": "mortgage",
                    "type": "loan",
                },
            ],
            "holdings": [
                {
                    "account_id": "jqpxEgMyoPH7qEdkdLnLIWRZkoNP1buZpalVK",
                    "cost_basis": 1,
                    "institution_price": 1,
                    "institution_price_as_of": None,
                    "institution_price_datetime": None,
                    "institution_value": 0.01,
                    "iso_currency_code": "USD",
                    "quantity": 0.01,
                    "security_id": "d6ePmbPxgWCWmMVv66q9iPV94n91vMtov5Are",
                    "unofficial_currency_code": None,
                },
                {
                    "account_id": "7MPwqV1ZrlUAq35b5VnVHxKmG64REpiMvxroy",
                    "cost_basis": 1.5,
                    "institution_price": 2.11,
                    "institution_price_as_of": None,
                    "institution_price_datetime": None,
                    "institution_value": 2.11,
                    "iso_currency_code": "USD",
                    "quantity": 1,
                    "security_id": "KDwjlXj1Rqt58dVvmzRguxJybmyQL8FgeWWAy",
                    "unofficial_currency_code": None,
                },
                {
                    "account_id": "7MPwqV1ZrlUAq35b5VnVHxKmG64REpiMvxroy",
                    "cost_basis": 10,
                    "institution_price": 10.42,
                    "institution_price_as_of": None,
                    "institution_price_datetime": None,
                    "institution_value": 20.84,
                    "iso_currency_code": "USD",
                    "quantity": 2,
                    "security_id": "NDVQrXQoqzt5v3bAe8qRt4A7mK7wvZCLEBBJk",
                    "unofficial_currency_code": None,
                },
                {
                    "account_id": "jqpxEgMyoPH7qEdkdLnLIWRZkoNP1buZpalVK",
                    "cost_basis": 0.01,
                    "institution_price": 0.011,
                    "institution_price_as_of": None,
                    "institution_price_datetime": None,
                    "institution_value": 110,
                    "iso_currency_code": "USD",
                    "quantity": 10000,
                    "security_id": "8E4L9XLl6MudjEpwPAAgivmdZRdBPJuvMPlPb",
                    "unofficial_currency_code": None,
                },
                {
                    "account_id": "7MPwqV1ZrlUAq35b5VnVHxKmG64REpiMvxroy",
                    "cost_basis": 120.03,
                    "institution_price": 39358.09375,
                    "institution_price_as_of": "2021-05-25",
                    "institution_price_datetime": None,
                    "institution_value": 115.57268,
                    "iso_currency_code": "USD",
                    "quantity": 0.00293644,
                    "security_id": "9EWp9Xpqk1ua6DyXQb89ikMARWA6eyUzAbPMg",
                    "unofficial_currency_code": None,
                },
                {
                    "account_id": "jqpxEgMyoPH7qEdkdLnLIWRZkoNP1buZpalVK",
                    "cost_basis": 40,
                    "institution_price": 42.15,
                    "institution_price_as_of": None,
                    "institution_price_datetime": None,
                    "institution_value": 210.75,
                    "iso_currency_code": "USD",
                    "quantity": 5,
                    "security_id": "abJamDazkgfvBkVGgnnLUWXoxnomp5up8llg4",
                    "unofficial_currency_code": None,
                },
                {
                    "account_id": "7MPwqV1ZrlUAq35b5VnVHxKmG64REpiMvxroy",
                    "cost_basis": 16,
                    "institution_price": 20,
                    "institution_price_as_of": None,
                    "institution_price_datetime": None,
                    "institution_value": 430,
                    "iso_currency_code": "USD",
                    "quantity": 21.5,
                    "security_id": "lngLy3Le7vflLnAzKqwZs19l6bl8P5H1jG9Zz",
                    "unofficial_currency_code": None,
                },
                {
                    "account_id": "7MPwqV1ZrlUAq35b5VnVHxKmG64REpiMvxroy",
                    "cost_basis": 23,
                    "institution_price": 27,
                    "institution_price_as_of": None,
                    "institution_price_datetime": None,
                    "institution_value": 636.309,
                    "iso_currency_code": "USD",
                    "quantity": 23.567,
                    "security_id": "JDdP7XPMklt5vwPmDN45t3KAoWAPmjtpaW7DP",
                    "unofficial_currency_code": None,
                },
                {
                    "account_id": "7MPwqV1ZrlUAq35b5VnVHxKmG64REpiMvxroy",
                    "cost_basis": 15,
                    "institution_price": 13.73,
                    "institution_price_as_of": None,
                    "institution_price_datetime": None,
                    "institution_value": 1373.6865,
                    "iso_currency_code": "USD",
                    "quantity": 100.05,
                    "security_id": "nnmo8doZ4lfKNEDe3mPJipLGkaGw3jfPrpxoN",
                    "unofficial_currency_code": None,
                },
                {
                    "account_id": "7MPwqV1ZrlUAq35b5VnVHxKmG64REpiMvxroy",
                    "cost_basis": 22,
                    "institution_price": 24.5,
                    "institution_price_as_of": None,
                    "institution_price_datetime": None,
                    "institution_value": 1855.875,
                    "iso_currency_code": "USD",
                    "quantity": 75.75,
                    "security_id": "MD9eKXeplrt5yKRlzLqXiavwb6wrdxUb3wdnM",
                    "unofficial_currency_code": None,
                },
                {
                    "account_id": "7MPwqV1ZrlUAq35b5VnVHxKmG64REpiMvxroy",
                    "cost_basis": 30,
                    "institution_price": 34.73,
                    "institution_price_as_of": None,
                    "institution_price_datetime": None,
                    "institution_value": 7397.49,
                    "iso_currency_code": "USD",
                    "quantity": 213,
                    "security_id": "eW4jmnjd6AtjxXVrjmj6SX1dNEdZp3Cy8RnRQ",
                    "unofficial_currency_code": None,
                },
                {
                    "account_id": "7MPwqV1ZrlUAq35b5VnVHxKmG64REpiMvxroy",
                    "cost_basis": 1,
                    "institution_price": 1,
                    "institution_price_as_of": None,
                    "institution_price_datetime": None,
                    "institution_value": 12345.67,
                    "iso_currency_code": "USD",
                    "quantity": 12345.67,
                    "security_id": "d6ePmbPxgWCWmMVv66q9iPV94n91vMtov5Are",
                    "unofficial_currency_code": None,
                },
            ],
            "item": {
                "available_products": [
                    "assets",
                    "balance",
                    "identity",
                    "recurring_transactions",
                    "transactions",
                ],
                "billed_products": ["investments"],
                "consent_expiration_time": None,
                "error": None,
                "institution_id": "ins_115616",
                "item_id": "37P61vejmdc1xgGPGLqLIENa7zoD8nCqqlbKR",
                "optional_products": None,
                "products": ["investments"],
                "update_type": "background",
                "webhook": "",
            },
            "request_id": "ku2tFvQoOGNyc02",
            "securities": [
                {
                    "close_price": 0.011,
                    "close_price_as_of": None,
                    "cusip": None,
                    "institution_id": None,
                    "institution_security_id": None,
                    "is_cash_equivalent": False,
                    "isin": None,
                    "iso_currency_code": "USD",
                    "name": "Nflx Feb 01'18 $355 Call",
                    "proxy_security_id": None,
                    "security_id": "8E4L9XLl6MudjEpwPAAgivmdZRdBPJuvMPlPb",
                    "sedol": None,
                    "ticker_symbol": "NFLX180201C00355000",
                    "type": "derivative",
                    "unofficial_currency_code": None,
                    "update_datetime": None,
                },
                {
                    "close_price": 39358.09375,
                    "close_price_as_of": "2021-05-25",
                    "cusip": None,
                    "institution_id": None,
                    "institution_security_id": None,
                    "is_cash_equivalent": True,
                    "isin": None,
                    "iso_currency_code": "USD",
                    "name": "Bitcoin",
                    "proxy_security_id": None,
                    "security_id": "9EWp9Xpqk1ua6DyXQb89ikMARWA6eyUzAbPMg",
                    "sedol": None,
                    "ticker_symbol": "CUR:BTC",
                    "type": "cash",
                    "unofficial_currency_code": None,
                    "update_datetime": None,
                },
                {
                    "close_price": 27,
                    "close_price_as_of": None,
                    "cusip": None,
                    "institution_id": None,
                    "institution_security_id": None,
                    "is_cash_equivalent": False,
                    "isin": None,
                    "iso_currency_code": "USD",
                    "name": "Matthews Pacific Tiger Fund Insti Class",
                    "proxy_security_id": None,
                    "security_id": "JDdP7XPMklt5vwPmDN45t3KAoWAPmjtpaW7DP",
                    "sedol": None,
                    "ticker_symbol": "MIPTX",
                    "type": "mutual fund",
                    "unofficial_currency_code": None,
                    "update_datetime": None,
                },
                {
                    "close_price": 2.11,
                    "close_price_as_of": None,
                    "cusip": None,
                    "institution_id": None,
                    "institution_security_id": None,
                    "is_cash_equivalent": False,
                    "isin": None,
                    "iso_currency_code": "USD",
                    "name": "Achillion Pharmaceuticals Inc.",
                    "proxy_security_id": None,
                    "security_id": "KDwjlXj1Rqt58dVvmzRguxJybmyQL8FgeWWAy",
                    "sedol": None,
                    "ticker_symbol": "ACHN",
                    "type": "equity",
                    "unofficial_currency_code": None,
                    "update_datetime": None,
                },
                {
                    "close_price": 24.5,
                    "close_price_as_of": None,
                    "cusip": None,
                    "institution_id": None,
                    "institution_security_id": None,
                    "is_cash_equivalent": False,
                    "isin": None,
                    "iso_currency_code": "USD",
                    "name": "Cambiar International Equity Institutional",
                    "proxy_security_id": None,
                    "security_id": "MD9eKXeplrt5yKRlzLqXiavwb6wrdxUb3wdnM",
                    "sedol": None,
                    "ticker_symbol": "CAMYX",
                    "type": "mutual fund",
                    "unofficial_currency_code": None,
                    "update_datetime": None,
                },
                {
                    "close_price": 10.42,
                    "close_price_as_of": None,
                    "cusip": None,
                    "institution_id": None,
                    "institution_security_id": None,
                    "is_cash_equivalent": False,
                    "isin": None,
                    "iso_currency_code": "USD",
                    "name": "DoubleLine Total Return Bond Fund",
                    "proxy_security_id": None,
                    "security_id": "NDVQrXQoqzt5v3bAe8qRt4A7mK7wvZCLEBBJk",
                    "sedol": None,
                    "ticker_symbol": "DBLTX",
                    "type": "mutual fund",
                    "unofficial_currency_code": None,
                    "update_datetime": None,
                },
                {
                    "close_price": 27,
                    "close_price_as_of": None,
                    "cusip": None,
                    "institution_id": None,
                    "institution_security_id": None,
                    "is_cash_equivalent": False,
                    "isin": None,
                    "iso_currency_code": "USD",
                    "name": "T. Rowe Price Equity Income",
                    "proxy_security_id": None,
                    "security_id": "PDRMBVM8r3t5BA9NmJdKfPolGqlg8dtEGB37n",
                    "sedol": None,
                    "ticker_symbol": "PRFDX",
                    "type": "mutual fund",
                    "unofficial_currency_code": None,
                    "update_datetime": None,
                },
                {
                    "close_price": 42.15,
                    "close_price_as_of": None,
                    "cusip": None,
                    "institution_id": None,
                    "institution_security_id": None,
                    "is_cash_equivalent": False,
                    "isin": None,
                    "iso_currency_code": "USD",
                    "name": "iShares Inc MSCI Brazil",
                    "proxy_security_id": None,
                    "security_id": "abJamDazkgfvBkVGgnnLUWXoxnomp5up8llg4",
                    "sedol": None,
                    "ticker_symbol": "EWZ",
                    "type": "etf",
                    "unofficial_currency_code": None,
                    "update_datetime": None,
                },
                {
                    "close_price": 1,
                    "close_price_as_of": None,
                    "cusip": None,
                    "institution_id": None,
                    "institution_security_id": None,
                    "is_cash_equivalent": True,
                    "isin": None,
                    "iso_currency_code": "USD",
                    "name": "U S Dollar",
                    "proxy_security_id": None,
                    "security_id": "d6ePmbPxgWCWmMVv66q9iPV94n91vMtov5Are",
                    "sedol": None,
                    "ticker_symbol": None,
                    "type": "cash",
                    "unofficial_currency_code": None,
                    "update_datetime": None,
                },
                {
                    "close_price": 34.73,
                    "close_price_as_of": None,
                    "cusip": None,
                    "institution_id": None,
                    "institution_security_id": None,
                    "is_cash_equivalent": False,
                    "isin": None,
                    "iso_currency_code": "USD",
                    "name": "Southside Bancshares Inc.",
                    "proxy_security_id": None,
                    "security_id": "eW4jmnjd6AtjxXVrjmj6SX1dNEdZp3Cy8RnRQ",
                    "sedol": None,
                    "ticker_symbol": "SBSI",
                    "type": "equity",
                    "unofficial_currency_code": None,
                    "update_datetime": None,
                },
                {
                    "close_price": 20,
                    "close_price_as_of": None,
                    "cusip": None,
                    "institution_id": None,
                    "institution_security_id": None,
                    "is_cash_equivalent": False,
                    "isin": None,
                    "iso_currency_code": "USD",
                    "name": "Trp Equity Income",
                    "proxy_security_id": "PDRMBVM8r3t5BA9NmJdKfPolGqlg8dtEGB37n",
                    "security_id": "lngLy3Le7vflLnAzKqwZs19l6bl8P5H1jG9Zz",
                    "sedol": None,
                    "ticker_symbol": None,
                    "type": "mutual fund",
                    "unofficial_currency_code": None,
                    "update_datetime": None,
                },
                {
                    "close_price": 13.73,
                    "close_price_as_of": None,
                    "cusip": None,
                    "institution_id": "ins_12",
                    "institution_security_id": "NHX105509",
                    "is_cash_equivalent": False,
                    "isin": None,
                    "iso_currency_code": "USD",
                    "name": "NH PORTFOLIO 1055 (FIDELITY INDEX)",
                    "proxy_security_id": None,
                    "security_id": "nnmo8doZ4lfKNEDe3mPJipLGkaGw3jfPrpxoN",
                    "sedol": None,
                    "ticker_symbol": "NHX105509",
                    "type": "etf",
                    "unofficial_currency_code": None,
                    "update_datetime": None,
                },
            ],
        }

        formatted_data = []

        for holding in data["holdings"]:
            finished_object = {}
            finished_object["number_of_shares"] = holding["quantity"]
            finished_object["user_id"] = user_id
            for stock in data["securities"]:
                if stock["security_id"] == holding["security_id"]:
                    finished_object["stock_name"] = stock["name"]
                    finished_object["stock_ticker"] = stock["ticker_symbol"]
            formatted_data.append(finished_object)

        cur = connection.cursor()
        for item in formatted_data:
            temp_stock_name = item["stock_name"]
            temp_stock_ticker = item["stock_ticker"]
            temp_number_of_shares = item["number_of_shares"]
            temp_user_id_id = item["user_id"]
            # cur.execute(
            #     f"INSERT INTO stockwatch_api_holding (stock_name, stock_ticker, number_of_shares, user_id_id) VALUES ('{temp_stock_name}', '{temp_stock_ticker}', {temp_number_of_shares}, (SELECT id FROM auth_api_useraccount WHERE id={temp_user_id_id}) )"
            # )
            h = Holding.objects.create(
                stock_name=temp_stock_name,
                stock_ticker=temp_stock_ticker,
                number_of_shares=temp_number_of_shares,
                user_id_id=temp_user_id_id,
            )

        return JsonResponse({})
