# Generated by Django 3.0.4 on 2020-04-16 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20200416_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordereditem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_items', to='product.Order'),
        ),
    ]
