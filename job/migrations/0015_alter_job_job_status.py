# Generated by Django 4.2.1 on 2023-07-25 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0014_alter_job_job_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_status',
            field=models.CharField(choices=[('1', 'Draft'), ('2', 'Active'), ('3', 'Deactivate'), ('4', 'Deleted')], default=2, max_length=100),
        ),
    ]