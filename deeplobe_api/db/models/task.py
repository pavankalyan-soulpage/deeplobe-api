from django.db import models
from ..mixins import TimeAuditModel
from django.db.models import JSONField
from django.conf import settings

class Task(TimeAuditModel):
    """[summary]
    Args:
        TimeAuditModel ([type]): [description]
    """

    # task uuid
    uuid = models.CharField(max_length=255)

    # name
    weight_name = models.CharField(max_length=255, blank=True)

    # kind of task
    task_type = models.CharField(max_length=255, blank=True)

    # user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # finished task
    task_finished = models.BooleanField(default=False)

    # data
    data = JSONField(blank=True, null=True)

    # extra
    extra = JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        db_table = "tasks"

    def __str__(self):
        return f"{self.user.email}/ {self.weight_name}/ {self.uuid}"