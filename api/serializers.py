from rest_framework import serializers
from .models import User
from .Serializers import *


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # code = serializers.CharField(style={'base_template': 'textarea.html'})
    # linenos = serializers.BooleanField(required=False)
    # language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    # style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    username  = serializers.CharField(max_length=100, allow_blank=False) #serializers.DateTimeField(auto_now_add=True)
    password  = serializers.CharField(max_length=100, allow_blank=False)
    email  = serializers.CharField(max_length=100, allow_blank=False)
    first_name  = serializers.CharField(max_length=100, allow_blank=False) 
    last_name  = serializers.CharField(max_length=100, allow_blank=False) #serializers.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    is_superuser  = serializers.BooleanField(required=False) # serializers.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    is_staff = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `User` instance, given the validated data.
        """
        # instance.title = validated_data.get('title', instance.title)
        # instance.code = validated_data.get('code', instance.code)
        # instance.linenos = validated_data.get('linenos', instance.linenos)
        # instance.language = validated_data.get('language', instance.language)
        # instance.style = validated_data.get('style', instance.style)
        
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        
        instance.save()
        return instance