# Generated by Django 3.2.6 on 2021-09-10 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_istrue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='isTrue',
        ),
    ]
