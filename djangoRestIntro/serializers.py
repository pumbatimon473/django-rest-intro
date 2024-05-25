from .models import User, Post
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # ('id', 'username', 'email', 'password', 'first_name', 'last_name')
