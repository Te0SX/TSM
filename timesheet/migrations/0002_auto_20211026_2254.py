# Generated by Django 3.2.8 on 2021-10-26 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='payment',
            field=models.IntegerField(default=5, verbose_name='Payperhour'),
        ),
        migrations.AddField(
            model_name='student',
            name='telephone',
            field=models.IntegerField(blank=True, null=True, verbose_name='Phone Number'),
        ),
    ]
