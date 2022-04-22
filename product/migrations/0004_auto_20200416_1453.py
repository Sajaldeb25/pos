# Generated by Django 3.0.4 on 2020-04-16 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20200416_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordereditem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='ordered_item_order', to='product.Order'),
        ),
    ]
