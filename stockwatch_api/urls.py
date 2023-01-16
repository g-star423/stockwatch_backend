from django.urls import path
from . import views

urlpatterns = [
    path("api/holdings", views.HoldingList.as_view(), name="holdings_list"),
    path("api/holdings/<int:pk>", views.HoldingDetail.as_view(), name="holding_detail"),
    path("api/traderequest", views.TradeList.as_view(), name="trade_list"),
    path("api/traderequest/<int:pk>", views.TradeDetail.as_view(), name="trade_detail"),
    path(
        "api/userholdings/<int:user_id>",
        views.HoldingsByUser.as_view(),
        name="user_holdings",
    ),
    path(
        "api/userrequests/<int:user_id>",
        views.RequestsByUser.as_view(),
        name="user_requests",
    ),
]
