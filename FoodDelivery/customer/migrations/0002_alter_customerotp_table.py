# Generated by Django 4.2.13 on 2024-06-22 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="customerotp",
            table="fd_customer_otp",
        ),
    ]
