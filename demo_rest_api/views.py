# views.py - Versión completa con debugging para PUT

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False})

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request, format=None):
        # Filtra la lista para incluir solo los elementos donde 'is_active' es True
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        # Validación: Comprueba que 'name' y 'email' estén presentes
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos: "name" y "email".'}, status=status.HTTP_400_BAD_REQUEST)

        # Si los campos son válidos:
        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)

        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
    """
    Vista para manejar operaciones sobre un item específico por su ID.
    """

    def get_item_by_id(self, item_id):
        """Función auxiliar para encontrar un item por su ID en data_list."""
        print(f"🔍 Buscando item con ID: {item_id}")
        print(f"📋 Items disponibles: {[item['id'] for item in data_list]}")
        
        for item in data_list:
            if item.get('id') == item_id:
                print(f"✅ Item encontrado: {item}")
                return item
        
        print("❌ Item no encontrado")
        return None

    def get(self, request, item_id):
        print(f"🔍 GET request para item_id: {item_id}")
        item = self.get_item_by_id(item_id)
        if item is None:
            return Response({'error': 'Item no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(item, status=status.HTTP_200_OK)

    def put(self, request, item_id):
        print(f"🔄 PUT request para item_id: {item_id}")
        print(f"📤 Datos recibidos: {request.data}")
        
        # Obtener el item por ID
        item_to_update = self.get_item_by_id(item_id)
        if item_to_update is None:
            print("❌ Item no encontrado para actualizar")
            return Response({'error': 'Item no encontrado para actualizar.'}, status=status.HTTP_404_NOT_FOUND)

        new_data = request.data
        print(f"📝 Datos para actualizar: {new_data}")

        # Validación de campos requeridos
        if 'name' not in new_data or 'email' not in new_data:
            print("❌ Faltan campos requeridos")
            return Response({'error': 'Faltan campos requeridos (name, email) para la actualización completa (PUT).'}, status=status.HTTP_400_BAD_REQUEST)

        # Reemplazo completo de datos
        print(f"📋 Item antes de actualizar: {item_to_update}")
        item_to_update['name'] = new_data['name']
        item_to_update['email'] = new_data['email']
        item_to_update['is_active'] = new_data.get('is_active', item_to_update.get('is_active', True))
        print(f"✅ Item después de actualizar: {item_to_update}")

        return Response({'message': 'Item actualizado completamente.', 'data': item_to_update}, status=status.HTTP_200_OK)

    def patch(self, request, item_id):
        print(f"🔧 PATCH request para item_id: {item_id}")
        
        item_to_update = self.get_item_by_id(item_id)
        if item_to_update is None:
            return Response({'error': 'Item no encontrado para actualización parcial.'}, status=status.HTTP_404_NOT_FOUND)

        patch_data = request.data
        print(f"📝 Datos para patch: {patch_data}")

        # Actualizar parcialmente los campos
        for key, value in patch_data.items():
            if key != 'id':
                item_to_update[key] = value

        return Response({'message': 'Item actualizado parcialmente.', 'data': item_to_update}, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        print(f"🗑️ DELETE request para item_id: {item_id}")
        
        # Buscar el índice del item para eliminar
        item_found_index = -1
        for i, item in enumerate(data_list):
            if item.get('id') == item_id:
                item_found_index = i
                break

        if item_found_index == -1:
            return Response({'error': 'Item no encontrado para eliminar.'}, status=status.HTTP_404_NOT_FOUND)
        
        data_list[item_found_index]['is_active'] = False 
        print(f"✅ Item marcado como inactivo: {data_list[item_found_index]}")

        return Response({'message': 'Item eliminado lógicamente (marcado como inactivo).'}, status=status.HTTP_200_OK)