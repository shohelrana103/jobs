# Generated by Django 3.2.4 on 2023-07-15 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0016_auto_20230715_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='about_company',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_website',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]