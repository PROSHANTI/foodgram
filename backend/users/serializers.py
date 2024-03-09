from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import Follow

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'email', 'id', 'password', 'username', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class FollowCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    author = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())

    class Meta:
        model = Follow
        fields = ['user', 'author']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset = Follow.objects.all(),
                fields = ['user', 'author'],
                message = "Вы не можете подписываться на самого себя."
            )
        ]

    def validate_author(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError(
                "Вы не можете подписываться на самого себя."
            )
        if Follow.objects.filter(
                user = self.context['request'].user, author = value
        ).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на данного пользователя."
            )
        return value

    def create(self, validated_data):
        return Follow.objects.create(**validated_data)
