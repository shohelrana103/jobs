# Generated by Django 4.2.1 on 2023-09-17 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0016_alter_job_industry'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
