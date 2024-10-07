import json
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import mixins
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from djangochannelsrestframework.observer import model_observer
from .models import *
from .serializers import *


class UserCreateConsumer(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAsyncAPIConsumer):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RoomConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = 'id'
    permission_classes = ()

    #actions
    @action()
    async def join_room(self, pk, **kwargs):
        self.room_subscribe = pk
        await self.add_user_to_room(pk)
        await self.notify_users()

    @action()
    async def leave_room(self, pk, **kwargs):
        await self.remove_user_from_room(pk)

    @action()
    async def new_message(self, message, **kwargs):

        await self.create_message(message=message)

    @action()
    async def subscribe_to_messages_in_room(self, pk, **kwargs):
        await self.message_activity.subscribe(room=pk)



    #async func

    async def disconnect(self, code):
        if hasattr(self, 'room_subscribe'):
            await  self.remove_user_from_room(self.room_subscribe)
            await  self.notify_users()
        await super().disconnect(code)

    async def notify_users(self):
        room: Room = await self.get_room(self.room_subscribe)
        for group in self.groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'update_users',
                    'cur_users': await self.current_users(room)
                }
            )

    #db func
    @database_sync_to_async
    def add_user_to_room(self, room_id):
        user: User = self.scope['user']
        room: Room = Room.objects.filter(pk=self.room_subscribe).first()
        if user not in room.users:
            room.users.add(user)

    @database_sync_to_async
    def get_room(self, pk: int):
        return Room.objects.get(pk=pk)

    @database_sync_to_async
    def current_users(self, room: Room):
        return [UserListSerializer(user).data for user in room.users.all()]

    @database_sync_to_async
    def remove_user_from_room(self, room_id):
        user: User = self.scope['user']
        room: Room = Room.objects.filter(pk=self.room_subscribe).first()
        room.users.remove(user)

    @database_sync_to_async
    def create_message(self, message):

        new_message = Message.objects.create(
            user = self.scope['user'],
            text = message
        )
        room: Room = Room.objects.filter(pk=self.room_subscribe).first()
        room.messages.add(new_message)