# Generated by Django 4.2.1 on 2023-06-12 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0009_remove_worker_is_profile_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='driving_license_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='worker',
            name='passport_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
