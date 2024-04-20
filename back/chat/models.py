from django.db import models
from django.contrib.auth.models import User as DjangoUser


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(DjangoUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in {self.room.name}: {self.content}"
