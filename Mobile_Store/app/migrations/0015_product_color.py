# Generated by Django 5.1.1 on 2024-10-25 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_product_detail_product_memory'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(choices=[('red', 'Red'), ('blue', 'Blue'), ('black', 'Black'), ('white', 'White'), ('green', 'Green')], default='black', max_length=10),
        ),
    ]