# Generated by Django 4.2.19 on 2025-03-04 09:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0009_alter_cartitem_cart_alter_cartitem_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="quantity",
            field=models.PositiveSmallIntegerField(
                validators=[django.core.validators.MinValueValidator(1)]
            ),
        ),
    ]
