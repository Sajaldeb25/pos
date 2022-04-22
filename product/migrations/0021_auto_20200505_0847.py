# Generated by Django 3.0.4 on 2020-05-05 02:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_auto_20200430_0420'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='product.Category'),
        ),
    ]