from django.contrib import admin

# Register your models here.
from .models.user import User
from .models.task import Task
from .models.task_status import TaskStatus
from .models.auth import SocialProvider

admin.site.register(User)
admin.site.register(Task)
admin.site.register(TaskStatus)
admin.site.register(SocialProvider)
