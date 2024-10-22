import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from typing import Any, Tuple, Dict, Optional, OrderedDict, Union

from django.db.models import Q
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import mixins
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin, action
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.permissions import IsAuthenticated
from rest_framework import status

from .models import *
from .serializers import *


class UserCreateConsumer(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAsyncAPIConsumer):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RoomConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = "pk"

    async def disconnect(self, code):
        if hasattr(self, "room_subscribe"):
            await self.remove_user_from_room(self.room_subscribe)
            await self.notify_users()
        await super().disconnect(code)

    @action()
    async def join_room(self, pk, **kwargs):
        self.room_subscribe = pk
        await self.add_user_to_room(pk)
        await self.notify_users()

    @action()
    async def leave_room(self, pk, **kwargs):
        await self.remove_user_from_room(pk)

    @action()
    async def create_message(self, message, **kwargs):
        room: Room = await self.get_room(pk=self.room_subscribe)
        await database_sync_to_async(Message.objects.create)(
            room=room,
            user=self.scope["user"],
            text=message
        )

    @action()
    async def update_message(self, message, message_id, **kwargs):
        await self.update_message(pk=message_id, text=message, user=self.scope['user'].id)

    @action()
    async def delete_message(self, message_id, **kwargs):
        await self.delete_message(pk=message_id, user=self.scope['user'].id)

    @action()
    async def subscribe_to_messages_in_room(self, pk, **kwargs):
        await self.message_activity.subscribe(room=pk)

    @model_observer(Message)
    async def message_activity(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @message_activity.groups_for_signal
    def message_activity(self, instance: Message, **kwargs):
        yield f'room__{instance.room_id}'
        yield f'pk__{instance.pk}'

    @message_activity.groups_for_consumer
    def message_activity(self, room=None, **kwargs):
        if room is not None:
            yield f'room__{room}'

    @message_activity.serializer
    def message_activity(self, instance: Message, action, **kwargs):
        return dict(data=MessageSerializer(instance).data, action=action.value, pk=instance.pk)

    async def notify_users(self):
        room: Room = await self.get_room(self.room_subscribe)
        for group in self.groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'update_users',
                    'usuarios': await self.current_users(room)
                }
            )

    async def update_users(self, event: dict):
        await self.send(text_data=json.dumps({'usuarios': event["usuarios"]}))

    @database_sync_to_async
    def get_room(self, pk: int) -> Room:
        return Room.objects.get(pk=pk)

    @database_sync_to_async
    def update_message(self, pk: int, text: str, user: int) -> None:
        message: Message = Message.objects.get(Q(pk=pk) & Q(user=user))
        if message:
            message.text = text
            message.save()

    @database_sync_to_async
    def delete_message(self, pk: int, user: int) -> None:
        message: Message = Message.objects.get(Q(pk=pk) & Q(user=user))
        if message:
            message.delete()

    @database_sync_to_async
    def current_users(self, room: Room):
        return [UserSerializer(user).data for user in room.current_users.all()]

    @database_sync_to_async
    def remove_user_from_room(self, room):
        user: User = self.scope["user"]
        user.current_rooms.remove(room)

    @database_sync_to_async
    def add_user_to_room(self, pk):
        user: User = self.scope["user"]
        if not user.current_rooms.filter(pk=self.room_subscribe).exists():
            user.current_rooms.add(Room.objects.get(pk=pk))


class CreateRoomConsumer(mixins.CreateModelMixin, GenericAsyncAPIConsumer):
    queryset = Room.objects.all()
    serializer_class = CreateUpdateRoomSerializer
    permission_classes = (IsAuthenticated,)

    @action()
    def create(self, data: dict, **kwargs):
        data['host'] = self.scope['user'].id
        serializer = self.get_serializer(data=data, action_kwargs=kwargs)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, **kwargs)

        return serializer.data, status.HTTP_201_CREATED


class RetrieveUpdateDeleteRoomConsumer(mixins.RetrieveModelMixin, mixins.PatchModelMixin, mixins.DeleteModelMixin,
                                       GenericAsyncAPIConsumer):
    queryset = Room.objects.all()
    lookup_field = 'id'
    serializer_class = CreateUpdateRoomSerializer
    permission_classes = (IsAuthenticated,)

    @action()
    def patch(self, data: dict, **kwargs):
        instance = self.get_object(data=data, **kwargs)
        room = Room.objects.get(pk=instance.pk)
        if room.host != self.scope['user']:
            return None, status.HTTP_403_FORBIDDEN
        serializer = self.get_serializer(instance=instance, data=data, action_kwargs=kwargs, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_patch(serializer, **kwargs)
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return serializer.data, status.HTTP_200_OK

    @action()
    def delete(self, **kwargs) -> Tuple[None, int]:
        instance = self.get_object(**kwargs)
        room = Room.objects.get(pk=instance.pk)
        if room.host != self.scope['user']:
            return None, status.HTTP_403_FORBIDDEN
        self.perform_delete(instance, **kwargs)
        return None, status.HTTP_204_NO_CONTENT
