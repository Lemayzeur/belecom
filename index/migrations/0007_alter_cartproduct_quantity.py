# Generated by Django 4.1 on 2022-09-23 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_cart_order_paymenttype_stock_payment_orderproduct_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
