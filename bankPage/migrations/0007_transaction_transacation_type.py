# Generated by Django 4.1 on 2023-06-20 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bankPage", "0006_rename_balance_balance_total_balance"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="transacation_type",
            field=models.CharField(default="", max_length=150),
        ),
    ]
