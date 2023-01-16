from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/tokens", views.UserTokenList.as_view(), name="token_list"
    ),  # api/contacts will be routed to the ContactList view for handling
    path(
        "api/tokens/<int:pk>", views.UserTokenDetail.as_view(), name="token_detail"
    ),  # api/contacts will be routed to the ContactDetail view for handling
]
