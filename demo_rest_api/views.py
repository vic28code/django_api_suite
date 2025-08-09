from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

# Simulación de base de datos local en memoria
data_list = []

# Datos iniciales de prueba
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False})  # Inactivo

# Función auxiliar para buscar elemento por ID
def find_item_by_id(item_id):
    return next((item for item in data_list if item['id'] == item_id), None)


class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)
        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)
        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
    def put(self, request, item_id):
        data = request.data or {}
        if 'id' not in data:
            return Response(
                {'message': 'El campo "id" es obligatorio en el cuerpo de la solicitud.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if data['id'] != item_id:
            return Response(
                {'message': 'El "id" del cuerpo no coincide con el "item_id" de la URL.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if 'name' not in data or 'email' not in data:
            return Response(
                {'message': 'Faltan campos requeridos: name y email.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        item = find_item_by_id(item_id)
        if not item:
            return Response({'message': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        new_item = {
            'id': item_id,
            'name': data['name'],
            'email': data['email'],
            'is_active': data.get('is_active', item.get('is_active', True))
        }
        idx = data_list.index(item)
        data_list[idx] = new_item

        return Response(
            {'message': 'Elemento reemplazado exitosamente.', 'data': new_item},
            status=status.HTTP_200_OK
        )

    def patch(self, request, item_id):
        data = request.data or {}
        item = find_item_by_id(item_id)
        if not item:
            return Response({'message': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if 'id' in data and data['id'] != item_id:
            return Response(
                {'message': 'No se permite modificar el "id". Debe coincidir con la URL.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        allowed_fields = {'name', 'email', 'is_active'}
        for key, value in data.items():
            if key in allowed_fields:
                item[key] = value

        return Response(
            {'message': 'Elemento actualizado parcialmente.', 'data': item},
            status=status.HTTP_200_OK
        )

    def delete(self, request, item_id):
        item = find_item_by_id(item_id)
        if not item:
            return Response({'message': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if not item.get('is_active', True):
            return Response({'message': 'El elemento ya estaba inactivo.'}, status=status.HTTP_400_BAD_REQUEST)

        item['is_active'] = False
        return Response({'message': 'Elemento eliminado lógicamente.'}, status=status.HTTP_200_OK)