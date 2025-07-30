from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

# Create your views here.
class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "rules"  # Cambia este valor por el nombre real de la colección
    def get(self, request):
        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')
        # get: Obtiene todos los elementos de la col ección
        data = ref.get()

        # Devuelve un arreglo JSON
        return Response(data, status=status.HTTP_200_OK)

