# Generated by Django 2.2.1 on 2019-08-17 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0010_auto_20190817_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='motherdriverconnection',
            name='mother',
        ),
        migrations.AddField(
            model_name='motherdriverconnection',
            name='motherPhoneNumber',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
