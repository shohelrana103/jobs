# Generated by Django 4.2.1 on 2023-06-08 06:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authentication',
            fields=[
                ('auth_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('username', models.CharField(blank=True, max_length=100, unique=True)),
                ('password', models.CharField(blank=True, max_length=100, null=True, validators=[django.core.validators.MinLengthValidator(6)])),
                ('token', models.CharField(max_length=100)),
                ('user_type', models.CharField(choices=[('1', 'Company'), ('2', 'Worker')], max_length=100)),
                ('user_phone', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-auth_id'],
            },
        ),
        migrations.CreateModel(
            name='UserOtp',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('otp', models.IntegerField()),
                ('otp_send_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('auth_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.authentication')),
            ],
        ),
    ]
