# Generated by Django 4.1.4 on 2023-01-16 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth_api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("link_token", models.CharField(max_length=255)),
                ("token_status", models.CharField(max_length=255)),
                (
                    "user_id",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="auth_api.useraccount",
                    ),
                ),
            ],
        ),
    ]
