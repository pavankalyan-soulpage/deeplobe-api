from rest_framework import serializers

from deeplobe_api.db.models import TaskStatus

class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = [
            "id",
            "process_type",
            "process_status",
            "task",
            "data",
            "extra"
        ]
