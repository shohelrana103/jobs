# Generated by Django 4.2.1 on 2023-09-18 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0019_remove_job_salary_type_job_salary_type_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='zip_code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
