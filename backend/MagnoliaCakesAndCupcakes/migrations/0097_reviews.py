# Generated by Django 4.2.4 on 2024-10-15 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MagnoliaCakesAndCupcakes', '0096_merge_20240512_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('stars', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
    ]