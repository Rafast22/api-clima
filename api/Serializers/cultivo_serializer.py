from rest_framework import serializers
from ..Models.cultivo import Cultivo


class CultivoSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    create_date  = serializers.DateTimeField(required=False)
    update_date = serializers.DateTimeField(required=False)
    name = serializers.CharField(max_length=32, required=True)
    variety = serializers.CharField(max_length=32, required=True)
    cycle_duration = serializers.IntegerField(required=False)
    client_id = serializers.IntegerField(required=True)
    def create(self, validated_data):
        """
        Create and return a new `Cultivo` instance, given the validated data.
        """
        return Cultivo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Cultivo` instance, given the validated data.
        """
        
        instance.create_date = validated_data.get('create_date', instance.create_date)
        instance.update_date = validated_data.get('update_date', instance.update_date)
        instance.name = validated_data.get('name', instance.name)
        instance.variety = validated_data.get('variety', instance.variety)
        instance.cycle_duration = validated_data.get('cycle_duration', instance.cycle_duration)
        instance.client_id = validated_data.get('client_id', instance.client_id)
        
        instance.save()
        return instance
    
    class Meta:
        model = Cultivo
        fields = '__all__'
