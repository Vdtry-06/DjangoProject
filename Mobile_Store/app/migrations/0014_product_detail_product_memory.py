# Generated by Django 5.1.1 on 2024-10-25 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_remove_product_digital'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='detail',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='memory',
            field=models.CharField(choices=[('32GB', '32 GB'), ('64GB', '64 GB'), ('128GB', '128 GB'), ('256GB', '256 GB'), ('512GB', '512 GB'), ('1TB', '1 TB')], default='64GB', max_length=5),
        ),
    ]
