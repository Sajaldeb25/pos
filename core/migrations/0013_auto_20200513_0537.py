# Generated by Django 3.0.4 on 2020-05-12 23:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20200512_0657'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('delete_admin', 'Can delete an admin'), ('promote_admin', 'Can promote a staff to admin'), ('demote_admin', 'Can demote admin to staff'), ('promote_superuser', 'Can promote a staff or admin to superuser')]},
        ),
    ]