# Generated by Django 2.2.24 on 2021-10-26 12:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0002_shift_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='date',
            field=models.DateTimeField(default=datetime.date(2021, 10, 26), verbose_name='Date of work'),
        ),
    ]
