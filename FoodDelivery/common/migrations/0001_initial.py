# Generated by Django 4.2.13 on 2024-06-22 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomerAuthTokens",
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
                (
                    "access_token",
                    models.TextField(db_column="auth_access_token", null=True),
                ),
                (
                    "refresh_token",
                    models.TextField(db_column="auth_refresh_token", null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "fd_auth_tokens",
            },
        ),
        migrations.CreateModel(
            name="RestaurantAuthTokens",
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
                (
                    "access_token",
                    models.TextField(db_column="auth_access_token", null=True),
                ),
                (
                    "refresh_token",
                    models.TextField(db_column="auth_refresh_token", null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "fd_restaurant_auth_tokens",
            },
        ),
    ]
