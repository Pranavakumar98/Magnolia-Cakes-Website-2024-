# Generated by Django 4.2.4 on 2023-10-19 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MagnoliaCakesAndCupcakes', '0091_product_price_id_product_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userproductpurchase',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='MagnoliaCakesAndCupcakes.flavor'),
        ),
        migrations.AlterField(
            model_name='userpurchase',
            name='products',
            field=models.ManyToManyField(blank=True, through='MagnoliaCakesAndCupcakes.UserProductPurchase', to='MagnoliaCakesAndCupcakes.flavor'),
        ),
    ]
