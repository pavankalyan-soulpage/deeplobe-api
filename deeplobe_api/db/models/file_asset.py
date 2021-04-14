from django.db import models
from ..mixins import TimeAuditModel
class FileAsset(TimeAuditModel):
    name = models.CharField(max_length=255)
    asset = models.FileField(upload_to="deeplobe_ai/Datasets")

    def __str__(self):
        return self.name

