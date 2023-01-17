from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path(
        "api/tokens", views.UserTokenList.as_view(), name="token_list"
    ),  # api/contacts will be routed to the ContactList view for handling
    path(
        "api/tokens/<int:pk>", views.UserTokenDetail.as_view(), name="token_detail"
    ),  # api/contacts will be routed to the ContactDetail view for handling
    path("api/firsttoken", csrf_exempt(views.request_token), name="first_token"),
    path("api/exchangetoken", csrf_exempt(views.exchange_token), name="exchange_token"),
]
