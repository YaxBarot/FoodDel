# Generated by Django 5.0.2 on 2024-07-05 02:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantProfile',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('restaurant_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('restaurant_name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('Restaurant_type', models.CharField(choices=[('RESTRAUNT', 'Restraunt'), ('FAST_FOOD', 'Fast Food'), ('FAST_CASUAL', 'Fast Casual'), ('CASUAL_DINING', 'Casual Dining'), ('FINE_DINING', 'Fine Dining'), ('CAFE', 'Café or Bistro'), ('BUFFET', 'Buffet'), ('FOOD_TRUCK', 'Food Truck'), ('FAMILY_STYLE', 'Family Style'), ('POP_UP', 'Pop-up Restaurant'), ('ETHNIC', 'Ethnic Restaurant'), ('BRASSERIE', 'Brasserie'), ('PIZZERIA', 'Pizzeria'), ('STEAKHOUSE', 'Steakhouse'), ('SEAFOOD', 'Seafood Restaurant'), ('VEGETARIAN_VEGAN', 'Vegetarian/Vegan Restaurant')], default='RESTRAUNT', max_length=255)),
                ('credit', models.CharField(default='0', max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
            options={
                'db_table': 'fd_restaurant_profile',
            },
        ),
        migrations.CreateModel(
            name='RestaurantOTP',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('restaurant_otp_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('otp', models.CharField(max_length=255)),
                ('restaurant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurantprofile')),
            ],
            options={
                'db_table': 'fd_restaurant_otp',
            },
        ),
    ]
