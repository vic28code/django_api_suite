
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
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request, format=None):
        # Filtra la lista para incluir solo los elementos donde 'is_active' es True
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data # Extrae los datos enviados en el cuerpo de la solicitud

        # Validación: Comprueba que 'name' y 'email' estén presentes
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos: "name" y "email".'}, status=status.HTTP_400_BAD_REQUEST)

        # Si los campos son válidos:
        # Generar un identificador único y asignarlo al campo 'id'
        data['id'] = str(uuid.uuid4())
        # Agregue el campo 'is_active' con el valor True
        data['is_active'] = True
        # Agregue la variable data a la lista data_list
        data_list.append(data)

        # Retornar una respuesta con código HTTP 201 (Created), mensaje de éxito y los datos guardados.
        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


# --- CLASE DemoRestApiItem para GET (individual), PUT, PATCH, DELETE ---
class DemoRestApiItem(APIView):
    """
    Vista para manejar operaciones sobre un item específico por su ID.
    """

    def get_item_by_id(self, item_id):
        """Función auxiliar para encontrar un item por su ID en data_list."""
        for item in data_list:
            if item.get('id') == item_id:
                return item
        return None # No se encontró el item

    # GET para un item específico (ej: /demo/rest/api/123e4567-e89b-12d3-a456-426614174000/)
    def get(self, request, item_id):
        item = self.get_item_by_id(item_id)
        if item is None:
            return Response({'error': 'Item no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(item, status=status.HTTP_200_OK)


    def put(self, request, item_id):
        # Obtener el item por ID
        item_to_update = self.get_item_by_id(item_id)
        if item_to_update is None:
            return Response({'error': 'Item no encontrado para actualizar.'}, status=status.HTTP_404_NOT_FOUND)

        new_data = request.data

        # Validación: Asegurarse de que 'name' y 'email' estén presentes para la actualización completa
        if 'name' not in new_data or 'email' not in new_data:
            return Response({'error': 'Faltan campos requeridos (name, email) para la actualización completa (PUT).'}, status=status.HTTP_400_BAD_REQUEST)

        # Reemplazar completamente los datos del elemento (excepto el ID)
        item_to_update['name'] = new_data['name']
        item_to_update['email'] = new_data['email']
        # Si quieres permitir que 'is_active' se cambie, usa new_data.get. Si no, omite esta línea.
        item_to_update['is_active'] = new_data.get('is_active', item_to_update.get('is_active', True))


        return Response({'message': 'Item actualizado completamente.', 'data': item_to_update}, status=status.HTTP_200_OK)


    def patch(self, request, item_id):
        # Obtener el item por ID
        item_to_update = self.get_item_by_id(item_id)
        if item_to_update is None:
            return Response({'error': 'Item no encontrado para actualización parcial.'}, status=status.HTTP_404_NOT_FOUND)

        patch_data = request.data

        # Actualizar parcialmente los campos
        for key, value in patch_data.items():
            if key != 'id': # No permitir cambio de ID desde la solicitud
                item_to_update[key] = value

        return Response({'message': 'Item actualizado parcialmente.', 'data': item_to_update}, status=status.HTTP_200_OK)


    def delete(self, request, item_id):
        # Buscar el índice del item para eliminar
        item_found_index = -1
        for i, item in enumerate(data_list):
            if item.get('id') == item_id:
                item_found_index = i
                break

        if item_found_index == -1:
            return Response({'error': 'Item no encontrado para eliminar.'}, status=status.HTTP_404_NOT_FOUND)
        data_list[item_found_index]['is_active'] = False 

        return Response({'message': 'Item eliminado lógicamente (marcado como inactivo).'}, status=status.HTTP_200_OK)