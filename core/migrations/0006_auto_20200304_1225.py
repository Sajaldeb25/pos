# Generated by Django 3.0.3 on 2020-03-04 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200304_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]
