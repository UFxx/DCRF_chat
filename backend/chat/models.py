from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from autoslug import AutoSlugField
from sortedm2m.fields import SortedManyToManyField


# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=15, verbose_name='Номер телефона', unique=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.phone}"

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


class Room(models.Model):
    ROOM_TYPE = (
        ('user_chat', 'user_chat'),
        ('group_chat', 'group_chat')
    )

    type = models.CharField(max_length=30, choices=ROOM_TYPE, default='user_chat')
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    users = SortedManyToManyField(User, verbose_name='Пользователи', blank=True)
    messages = SortedManyToManyField('Message', verbose_name='Сообщения', blank=True)
    slug = AutoSlugField(populate_from='create_url', unique=True, verbose_name='URL')

    def __str__(self):
        return f"Room-{self.name}#{self.pk}"

    def create_url(self):
        return f"{self.name}"


class Message(models.Model):
    text = models.TextField(verbose_name='Сообщение')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')

    def __str__(self):
        return f"Message {self.pk}"
