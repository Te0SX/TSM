# Generated by Django 2.2.24 on 2021-11-01 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0007_auto_20211027_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='shift',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
