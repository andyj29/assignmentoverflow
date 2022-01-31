import uuid
from django.db import models
from django.contrib import admin


class Notification(models.Model):
  id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  type = models.CharField(max_length=255, default='unknown')
  receiver = models.ForeignKey('authentication.User', related_name='notifications', on_delete=models.CASCADE, editable=False)
  is_read = models.BooleanField(default=False)
  initiated_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, editable=False)
  timestamp = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(self.timestamp)


admin.site.register(Notification)