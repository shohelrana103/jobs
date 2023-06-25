# Generated by Django 4.2.1 on 2023-06-25 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0011_workershortlistedjob'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobapplication',
            options={'verbose_name_plural': 'My Applied Jobs'},
        ),
        migrations.AddField(
            model_name='worker',
            name='video_resume',
            field=models.FileField(blank=True, null=True, upload_to='worker/video'),
        ),
    ]
