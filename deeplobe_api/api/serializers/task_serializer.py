from rest_framework import serializers

from deeplobe_api.db.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "uuid",
            "weight_name",
            "task_type",
            "user",
            "task_finished",
            "data",
            "extra"
        ]

