# Generated by Django 3.2.4 on 2023-06-09 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_gender'),
        ('worker', '0007_worker_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='is_profile_set',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='worker',
            name='address_line1',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='worker',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.city'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.country'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='worker',
            name='gender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.gender'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
