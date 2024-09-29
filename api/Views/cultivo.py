from django.shortcuts import render
from ..Serializers.cultivo_serializer import CultivoSerializer
from ..Models.cultivo import Cultivo
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def cultivo_list_by_client_id(request, pk=0):
    """
    List all code cultivo, or create a new cultivo.
    """
    if request.method == 'GET':
        cultivo = Cultivo.objects.all()
        serializer = CultivoSerializer(cultivo, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CultivoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
@csrf_exempt
def cultivo_detail(request, pk):
    """
    Retrieve, update or delete a code cultivo.
    """
    try:
        cultivo = Cultivo.objects.get(pk=pk)
    except Cultivo.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CultivoSerializer(cultivo)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CultivoSerializer(cultivo, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        cultivo.delete()
        return HttpResponse(status=204)