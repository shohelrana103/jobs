from django.db import models
from rest_framework import serializers


class Skill(models.Model):
    id = models.BigAutoField(primary_key=True)
    skill_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.skill_name


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'skill_name')
