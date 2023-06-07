# Generated by Django 4.2.1 on 2023-06-05 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_degree_alter_city_options_alter_country_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('gender_name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Genders',
            },
        ),
    ]