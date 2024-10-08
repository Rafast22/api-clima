from django.shortcuts import render
from ..Serializers.client_serializer import ClientSerializer
from ..Serializers.cultivo_serializer import CultivoSerializer
from ..Models.client import Client
from ..Models.cultivo import Cultivo
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import status


class ClientList(generics.ListCreateAPIView):
    serializer_class = ClientSerializer
    def post(self, request, format=None):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return JsonResponse(obj.id, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        client = Client.objects.all()
        serializer = ClientSerializer(client, many=True)
        return JsonResponse(serializer.data, safe=False)
    
@csrf_exempt
def client_detail(request, pk):
    """
    Retrieve, update or delete a code client.
    """
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ClientSerializer(client)
        data = dict(serializer.data)
        # cultivos = Cultivo.objects.all()
        # cultivoSerial = CultivoSerializer(cultivos)
        #data["cultivos"] = cultivoSerial.data
        return JsonResponse(data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ClientSerializer(client, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        client.delete()
        return HttpResponse(status=204)