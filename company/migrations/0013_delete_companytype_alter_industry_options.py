# Generated by Django 4.2.1 on 2023-06-07 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0012_company_industry'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CompanyType',
        ),
        migrations.AlterModelOptions(
            name='industry',
            options={'verbose_name_plural': 'Industries'},
        ),
    ]
