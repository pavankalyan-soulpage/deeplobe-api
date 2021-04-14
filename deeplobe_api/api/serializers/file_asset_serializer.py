from rest_framework import serializers
from deeplobe_api.db.models import FileAsset

class FileAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAsset
        fields = ("id", "name", "asset")