# Generated by Django 3.2.8 on 2021-10-27 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0005_auto_20211027_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='endHour',
            field=models.TimeField(verbose_name='Time finished working'),
        ),
        migrations.AlterField(
            model_name='shift',
            name='startHour',
            field=models.TimeField(verbose_name='Time started working'),
        ),
    ]