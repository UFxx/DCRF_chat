from rest_framework import serializers

from .models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'phone' )
        extra_kwargs = {'password': {'write_only': True}}

