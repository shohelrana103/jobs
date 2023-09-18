# Generated by Django 4.2.1 on 2023-09-15 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0018_company_company_email'),
        ('job', '0015_alter_job_job_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.industry'),
        ),
    ]