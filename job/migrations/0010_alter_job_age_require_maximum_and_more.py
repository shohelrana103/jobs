# Generated by Django 4.2.1 on 2023-06-19 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_gender'),
        ('job', '0009_job_job_placement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='age_require_maximum',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='age_require_minimum',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.city'),
        ),
        migrations.AlterField(
            model_name='job',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.country'),
        ),
        migrations.AlterField(
            model_name='job',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.state'),
        ),
    ]