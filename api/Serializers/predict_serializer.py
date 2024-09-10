from rest_framework import serializers
from ..Models.predict import Predict



class PredictSerializer(serializers.Serializer):
    
    date = serializers.CharField(max_length=11, allow_blank=False) #serializers.DateTimeField(auto_now_add=True)
    PRECTOTCORR = serializers.CharField(max_digits=10, decimal_places=2, null=True)
  
    
    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        """
        return Predict.objects.create(**validated_data)

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