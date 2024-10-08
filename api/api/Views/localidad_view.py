from django.shortcuts import render
from ..Serializers.localidad_serializer import LocalidadSerializer
from ..Models.client import Client
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny


class LocalidadRegistrationView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = LocalidadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocalidadGetView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = LocalidadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)