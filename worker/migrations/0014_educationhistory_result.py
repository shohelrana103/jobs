# Generated by Django 3.2.4 on 2023-07-15 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0013_workerfavoritejob'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationhistory',
            name='result',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]