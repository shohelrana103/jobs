# Generated by Django 4.2.1 on 2023-06-07 02:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0012_company_industry'),
        ('job', '0005_rename_age_restriction_job_age_require_maximum_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='industry',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='company.industry'),
            preserve_default=False,
        ),
    ]
