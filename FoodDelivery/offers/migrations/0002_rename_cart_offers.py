# Generated by Django 5.0.2 on 2024-07-09 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_menucategory_created_at_menucategory_is_deleted_and_more'),
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cart',
            new_name='Offers',
        ),
    ]