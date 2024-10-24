# Generated by Django 4.2.4 on 2023-10-18 14:35

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('MagnoliaCakesAndCupcakes', '0072_rename_cakecategory_gallerycategory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userpurchase',
            options={},
        ),
        migrations.RemoveField(
            model_name='userpurchase',
            name='cakes',
        ),
        migrations.CreateModel(
            name='UserVideoPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_purchase', models.ForeignKey(on_delete=models.deletion.CASCADE, to='MagnoliaCakesAndCupcakes.userpurchase')),
                ('video', models.ForeignKey(null=True, on_delete=models.deletion.SET_NULL, to='MagnoliaCakesAndCupcakes.video')),
            ],
        ),
        migrations.CreateModel(
            name='UserProductPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(null=True, on_delete=models.deletion.SET_NULL, to='MagnoliaCakesAndCupcakes.product')),
                ('user_purchase', models.ForeignKey(on_delete=models.deletion.CASCADE, to='MagnoliaCakesAndCupcakes.userpurchase')),
            ],
        ),
        migrations.CreateModel(
            name='UserCakePurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cake_variant', models.ForeignKey(null=True, on_delete=models.deletion.SET_NULL, to='MagnoliaCakesAndCupcakes.cakevariant')),
                ('user_purchase', models.ForeignKey(on_delete=models.deletion.CASCADE, to='MagnoliaCakesAndCupcakes.userpurchase')),
            ],
        ),
        migrations.AddField(
            model_name='userpurchase',
            name='cake_variant',
            field=models.ManyToManyField(blank=True, through='MagnoliaCakesAndCupcakes.UserCakePurchase', to='MagnoliaCakesAndCupcakes.cakevariant'),
        ),
        migrations.AddField(
            model_name='userpurchase',
            name='products',
            field=models.ManyToManyField(blank=True, through='MagnoliaCakesAndCupcakes.UserProductPurchase', to='MagnoliaCakesAndCupcakes.product'),
        ),
        # Remove the AlterField operation for the videos field
    ]
