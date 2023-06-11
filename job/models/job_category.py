from django.db import models
from rest_framework import serializers


class JobCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=200)
    category_icon = models.FileField(upload_to='job/category/icons/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Job Categories'

    def __str__(self):
        return self.category_name


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        exclude = ('created_at', 'updated_at')
