# Generated by Django 3.0.4 on 2020-05-11 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200305_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_no1',
            field=models.CharField(default='01767788288', max_length=11, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='phone_no2',
            field=models.CharField(default='01767788280', max_length=11, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
