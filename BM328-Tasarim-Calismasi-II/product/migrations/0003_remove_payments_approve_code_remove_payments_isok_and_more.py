# Generated by Django 4.2 on 2023-05-29 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_remove_coupon_order_id_remove_payments_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payments',
            name='approve_code',
        ),
        migrations.RemoveField(
            model_name='payments',
            name='isok',
        ),
        migrations.RemoveField(
            model_name='payments',
            name='payment_type',
        ),
    ]