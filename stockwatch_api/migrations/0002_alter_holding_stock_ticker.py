# Generated by Django 4.1.4 on 2023-01-18 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stockwatch_api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="holding",
            name="stock_ticker",
            field=models.CharField(max_length=9, null=True),
        ),
    ]
