# Generated by Django 2.2.24 on 2021-11-23 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Student', 'Student'), ('Verifier', 'Verifier'), ('Payer', 'Payer'), ('Admin', 'Admin')], max_length=100, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('salary', models.FloatField(default=0)),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.UserRoles')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
