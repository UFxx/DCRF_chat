from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from autoslug import AutoSlugField
from sortedm2m.fields import SortedManyToManyField


# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=15, verbose_name='Номер телефона', )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


class Room(models.Model):
    ROOM_TYPE = (
        ('user_chat', 'user_chat'),
        ('group_chat', 'group_chat')
    )

    name = models.CharField(max_length=255, )
    type = models.CharField(max_length=30, choices=ROOM_TYPE, default='user_chat')
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rooms", blank=True, null=True)
    current_users = models.ManyToManyField(User, related_name="current_rooms", blank=True)

    def __str__(self):
        return f"Room({self.name} {self.host})"


class Message(models.Model):
    room = models.ForeignKey("chat.Room", on_delete=models.CASCADE, related_name="messages", null=True, blank=True)
    text = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message({self.user} {self.room})"


