# Generated by Django 2.2.24 on 2021-11-08 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0008_auto_20211101_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timesheet.Roles'),
        ),
    ]
