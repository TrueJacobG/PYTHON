# Generated by Django 3.2.6 on 2021-09-01 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='isTrue',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
