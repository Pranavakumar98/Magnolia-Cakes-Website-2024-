# Generated by Django 4.2.4 on 2023-10-19 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MagnoliaCakesAndCupcakes', '0088_alter_termsandcondition_options_remove_flavor_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cakevariant',
            name='product_id_link',
            field=models.IntegerField(default='0', editable=False),
            preserve_default=False,
        ),
    ]
