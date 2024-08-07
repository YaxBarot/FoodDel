# Generated by Django 5.0.2 on 2024-07-10 06:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
        ('restaurant', '0003_restaurantprofile_no_of_ratings'),
    ]

    operations = [
        migrations.AddField(
            model_name='offers',
            name='restaurant_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurantprofile'),
            preserve_default=False,
        ),
    ]
