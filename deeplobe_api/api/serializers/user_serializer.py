from rest_framework import serializers

from deeplobe_api.db.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username"
            "email",
            "first_name",
            "last_name",
            "company",
            "job_title",
            "terms_conditions",
        ]

