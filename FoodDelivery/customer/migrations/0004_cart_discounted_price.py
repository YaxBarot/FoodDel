# Generated by Django 5.0.2 on 2024-07-10 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_cart_is_offer_applied_offershistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='discounted_price',
            field=models.CharField(default=0, max_length=255),
        ),
    ]
