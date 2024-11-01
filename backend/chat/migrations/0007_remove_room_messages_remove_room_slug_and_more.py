# Generated by Django 5.0.3 on 2024-10-20 19:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_alter_user_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='messages',
        ),
        migrations.RemoveField(
            model_name='room',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='room',
            name='users',
        ),
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.room'),
        ),
        migrations.AddField(
            model_name='room',
            name='current_users',
            field=models.ManyToManyField(blank=True, related_name='current_rooms', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='room',
            name='host',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
