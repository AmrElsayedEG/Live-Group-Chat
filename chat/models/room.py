from django.db import models
import uuid

class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, unique=True)
    current_users = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural  = 'Rooms'