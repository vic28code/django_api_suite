from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "encargos"

    def get(self, request):
        ref = db.reference(f'{self.collection_name}')
        data = ref.get()
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        ref = db.reference(f'{self.collection_name}')
        current_time = datetime.now()
        custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
        data.update({"timestamp": custom_format})

        new_resource = ref.push(data)
        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)
'''
class LandingAPIItem(APIView):
    collection_name = "encargos"

    def _item(self, item_id: str):
        return db.reference(f"{self.collection_name}/{item_id}")

    def get(self, request, item_id):
        ref = self._item(item_id)
        current = ref.get()
        if current is None:
            return Response({'message': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(current, status=status.HTTP_200_OK)

    # PUT: reemplazo total en Firebase. Exige id en body e igual a la URL.
    def put(self, request, item_id):
        data = dict(request.data or {})
        if 'id' not in data:
            return Response({'message': 'El campo "id" es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)
        if data['id'] != item_id:
            return Response({'message': 'El "id" del body debe coincidir con la URL.'}, status=status.HTTP_400_BAD_REQUEST)
        if 'name' not in data or 'email' not in data:
            return Response({'message': 'Faltan campos requeridos: name y email.'}, status=status.HTTP_400_BAD_REQUEST)

        ref = self._item(item_id)
        current = ref.get()
        if current is None:
            return Response({'message': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        new_item = {
            'id': item_id,
            'name': data['name'],
            'email': data['email'],
            'is_active': data.get('is_active', True),
            'timestamp': data.get('timestamp', current.get('timestamp', '')),
        }
        
        try:
            ref.set(new_item)  # reemplazo total en Firebase
            # Verificar que se guardó correctamente
            saved_item = ref.get()
            if saved_item:
                return Response({'message': 'Elemento reemplazado exitosamente.', 'data': saved_item}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Error al guardar en Firebase.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'message': f'Error al actualizar: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PATCH: actualización parcial en Firebase. No permite cambiar id.
    def patch(self, request, item_id):
        partial = dict(request.data or {})
        if 'id' in partial and partial['id'] != item_id:
            return Response({'message': 'No se permite modificar el "id".'}, status=status.HTTP_400_BAD_REQUEST)

        ref = self._item(item_id)
        current = ref.get()
        if current is None:
            return Response({'message': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        allowed = {'name', 'email', 'is_active', 'timestamp'}
        to_update = {k: v for k, v in partial.items() if k in allowed}
        if not to_update:
            return Response({'message': 'No hay campos válidos para actualizar.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ref.update(to_update)  # actualización parcial
            # Verificar que se actualizó correctamente
            updated_item = ref.get()
            if updated_item:
                return Response({'message': 'Elemento actualizado parcialmente.', 'data': updated_item}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Error al actualizar en Firebase.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'message': f'Error al actualizar: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DELETE: eliminación física directa
    def delete(self, request, item_id):
        ref = self._item(item_id)
        current = ref.get()
        if current is None:
            return Response({'message': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            ref.delete()
            # Verificar que se eliminó correctamente
            deleted_check = ref.get()
            if deleted_check is None:
                return Response({'message': f'Elemento {item_id} eliminado permanentemente.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Error: el elemento no se pudo eliminar completamente.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'message': f'Error al eliminar: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

'''

class LandingAPIItem(APIView):
    collection_name = "encargos"

    def _item(self, item_id: str):
        # referencia directa al nodo del item
        return db.reference(f"{self.collection_name}/{item_id}")

    def get(self, request, item_id):
        ref = self._item(item_id)
        data = ref.get()
        if data is None:
            return Response({"message": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        # devuelve el objeto incluyendo su id para comodidad
        return Response({"id": item_id, **data}, status=status.HTTP_200_OK)
    
    def put(self, request, item_id):
        data = dict(request.data or {})
        if 'id' not in data:
            return Response({'message': 'El campo "id" es obligatorio.'}, status=status.HTTP_400_BAD_REQUEST)
        if data['id'] != item_id:
            return Response({'message': 'El "id" del body debe coincidir con la URL.'}, status=status.HTTP_400_BAD_REQUEST)

        ref = self._item(item_id)
        if ref.get() is None:
            return Response({'message': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        # timestamp automático
        now = datetime.now()
        custom_format = now.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
        data['timestamp'] = custom_format

        ref.set(data)
        return Response({'message': 'Reemplazado correctamente.'}, status=status.HTTP_200_OK)

    def patch(self, request, item_id):
        """
        Actualización parcial del recurso.
        """
        ref = self._item(item_id)
        if ref.get() is None:
            return Response({'message': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        partial = dict(request.data or {})
        if 'id' in partial and partial['id'] != item_id:
            return Response({'message': 'No se permite cambiar el id.'}, status=status.HTTP_400_BAD_REQUEST)

        # timestamp automático
        now = datetime.now()
        custom_format = now.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
        partial['timestamp'] = custom_format

        ref.update(partial)
        return Response({'message': 'Actualizado correctamente.'}, status=status.HTTP_200_OK)

    def delete(self, request, item_id):
        ref = self._item(item_id)
        if ref.get() is None:
            return Response({'message': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        ref.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)