from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "encargos"

    def get(self, request, pk=None):
        ref = db.reference(f'{self.collection_name}')

        if pk:
            item_ref = ref.child(pk)
            item = item_ref.get()
            if item:
                return Response(item, status=status.HTTP_200_OK)
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

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

    def put(self, request, pk):
        data = request.data
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos: name y email.'}, status=status.HTTP_400_BAD_REQUEST)

        item_ref = db.reference(f'{self.collection_name}/{pk}')
        item = item_ref.get()

        if item:
            new_item = {
                'name': data['name'],
                'email': data['email'],
                'is_active': data.get('is_active', item.get('is_active', True)),
                'timestamp': item.get('timestamp', '')
            }
            item_ref.set(new_item)
            return Response({'message': 'Elemento reemplazado exitosamente.', 'data': new_item}, status=status.HTTP_200_OK)

        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        data = request.data
        item_ref = db.reference(f'{self.collection_name}/{pk}')
        item = item_ref.get()

        if item:
            item.update({k: v for k, v in data.items() if k != 'id'})
            item_ref.update(item)
            return Response({'message': 'Elemento actualizado parcialmente.', 'data': item}, status=status.HTTP_200_OK)

        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        item_ref = db.reference(f'{self.collection_name}/{pk}')
        item = item_ref.get()

        if item:
            if not item.get('is_active', True):
                return Response({'error': 'El elemento ya está inactivo.'}, status=status.HTTP_400_BAD_REQUEST)

            item_ref.update({'is_active': False})
            return Response({'message': 'Elemento eliminado lógicamente.'}, status=status.HTTP_200_OK)

        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
