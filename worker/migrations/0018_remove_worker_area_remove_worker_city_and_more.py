# Generated by Django 4.2.1 on 2023-09-19 07:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_zipaddress'),
        ('worker', '0017_rename_postal_code_worker_zip_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worker',
            name='area',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='city',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='country',
        ),
        migrations.RemoveField(
            model_name='worker',
            name='state',
        ),
        migrations.AddField(
            model_name='worker',
            name='zip_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.zipaddress'),
        ),
    ]
