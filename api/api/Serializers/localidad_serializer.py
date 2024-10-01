from rest_framework import serializers
from ..Models.localidad import Localidad


class LocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localidad
        fields = ['Latitude', 'Longitude', 'Client']
    def create(self, validated_data):
        return Localidad.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.Latitude = validated_data.get('Latitude', instance.Latitude)
        instance.Longitude = validated_data.get('Longitude', instance.Longitude)
        instance.Client = validated_data.get('Client', instance.Client)
        instance.save()
        return instance