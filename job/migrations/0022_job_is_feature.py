# Generated by Django 4.2.1 on 2023-10-19 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0021_remove_job_city_remove_job_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='is_feature',
            field=models.BooleanField(default=False),
        ),
    ]