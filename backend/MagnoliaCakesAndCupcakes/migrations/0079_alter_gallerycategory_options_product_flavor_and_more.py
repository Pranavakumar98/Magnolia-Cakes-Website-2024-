# Generated by Django 4.2.4 on 2023-10-19 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MagnoliaCakesAndCupcakes', '0078_alter_galleryitem_options_remove_product_flavor_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gallerycategory',
            options={'verbose_name_plural': 'Cake Categories'},
        ),
        migrations.AddField(
            model_name='product',
            name='flavor',
            field=models.CharField(default='vanilla', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cakevariant',
            name='cake',
            field=models.ForeignKey(limit_choices_to={'product_type': 'Cake'}, on_delete=django.db.models.deletion.CASCADE, related_name='size_prices', to='MagnoliaCakesAndCupcakes.product'),
        ),
        migrations.DeleteModel(
            name='Flavor',
        ),
    ]
