# Generated by Django 4.1.4 on 2023-01-18 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stockwatch_api", "0002_alter_holding_stock_ticker"),
    ]

    operations = [
        migrations.AlterField(
            model_name="holding",
            name="stock_ticker",
            field=models.CharField(max_length=255, null=True),
        ),
    ]