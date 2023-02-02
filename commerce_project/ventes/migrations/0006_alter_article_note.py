# Generated by Django 3.2.6 on 2023-01-30 13:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventes', '0005_shopperpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='note',
            field=models.FloatField(blank=True, default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]
