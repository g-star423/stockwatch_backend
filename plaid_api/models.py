from django.db import models

# Create your models here.
class UserToken(models.Model):
    link_token = models.CharField(max_length=255, blank=True)
    token_status = models.CharField(
        max_length=255, blank=True
    )  # used for testing purpose, values should be "blank, on way to Plaid", "received from plaid on way to client", "back from client, sending to Plaid for persistant token", "final persistant token"
    user_id = models.ForeignKey(
        "auth_api.UserAccount", on_delete=models.CASCADE, default=None
    )
