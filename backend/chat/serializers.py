from rest_framework import serializers

from .models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'phone' )
        extra_kwargs = {'password': {'write_only': True}}


class UserListSerializer(serializers.ModelSerializer):
    model = User
    fields = ('id', 'username', 'phone')


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username',  )
    class Meta:
        model = Message
        fields = ('id', 'text', 'user', 'created_at')
class RoomSerializer(serializers.ModelSerializer):

    users = UserListSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ('id', 'name', 'users', 'slug')

        

