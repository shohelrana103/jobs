# Generated by Django 4.2.1 on 2023-06-01 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_job'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='company',
        ),
    ]
