from django.db import models
import uuid


class MineSweeper(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    mines_count = models.IntegerField()
    field = models.JSONField(null=True, blank=True)
    open_field = models.JSONField(null=True, blank=True)
    game_id = models.UUIDField(default=uuid.uuid4)
    completed = models.BooleanField(default=False)
