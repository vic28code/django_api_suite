from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

# Create your views here.
class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "nombre_de_la_coleccion"  # Cambia este valor por el nombre real de la colección
