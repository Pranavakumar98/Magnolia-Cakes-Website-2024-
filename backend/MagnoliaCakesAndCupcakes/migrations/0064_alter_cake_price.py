# Generated by Django 4.2.4 on 2023-10-16 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MagnoliaCakesAndCupcakes', '0063_alter_cakesizeprice_cake'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cake',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
