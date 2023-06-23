# Generated by Django 4.2.1 on 2023-06-21 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0011_alter_job_degree_requirements'),
        ('worker', '0010_worker_driving_license_number_worker_passport_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkerShortListedJob',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.job')),
                ('worker_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='worker.worker')),
            ],
        ),
    ]