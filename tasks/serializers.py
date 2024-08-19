from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    due_date = serializers.DateField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


    def create(self, validated_data: dict):
        return Task.objects.create(**validated_data)
    
    
    def update(self, instance: Task, validated_data: dict):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description',instance.description)
        instance.due_date = validated_data.get('due_date', instance.due_date)

        instance.save()

        return instance
    
