# Generated by Django 5.0.2 on 2024-06-23 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantprofile',
            name='Restaurant_type',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
