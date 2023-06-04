# Generated by Django 4.2.1 on 2023-06-04 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_area'),
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='job_location',
        ),
        migrations.AddField(
            model_name='job',
            name='job_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.area'),
        ),
    ]