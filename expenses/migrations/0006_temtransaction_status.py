# Generated by Django 4.2.5 on 2023-10-02 18:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0005_alter_transaction_amount_alter_transaction_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="temtransaction",
            name="status",
            field=models.IntegerField(null=True),
        ),
    ]
