# Generated by Django 5.1.1 on 2024-10-20 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_remove_shippingaddress_feedback_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='digital',
        ),
    ]
