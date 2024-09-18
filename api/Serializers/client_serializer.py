from rest_framework import serializers
from ..Models.client import Client



class ClientSerializer(serializers.Serializer):
    
    id = serializers.IntegerField(required=False)
    create_date = serializers.DateTimeField(required=False)
    update_date = serializers.DateTimeField(required=False)
    
    def create(self, validated_data):
        """
        Create and return a new `Client` instance, given the validated data.
        """
        return Client.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Client` instance, given the validated data.
        """
        
        instance.create_date = validated_data.get('create_date', instance.create_date)
        instance.update_date = validated_data.get('update_date', instance.update_date)
        instance.name = validated_data.get('name', instance.name)
        instance.variety = validated_data.get('variety', instance.variety)
        instance.cycle_duration = validated_data.get('cycle_duration', instance.cycle_duration)
        instance.client_id = validated_data.get('client_id', instance.client_id)
        
        instance.save()
        return instance