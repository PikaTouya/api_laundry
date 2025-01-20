from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pos_app.models import TableUser, TableOrder
from api.serializers import TableUserSerializers, TableOrderSerializers, GetTableOrderSerializers, RegisterSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

class TableUserListApiView(APIView):
    permission_classes = [AllowAny]  # Mengizinkan akses tanpa autentikasi

    def get(self, request, *args, **kwargs):
        table_user = TableUser.objects.all()
        serializer = TableUserSerializers(table_user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = TableUserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User successfully created.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TableUserDetailApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, *args, **kwargs):
        try:
            user = TableUser.objects.get(id=id)
        except TableUser.DoesNotExist:
            return Response({'message': f'User with id {id} not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TableUserSerializers(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        try:
            user = TableUser.objects.get(id=id)
        except TableUser.DoesNotExist:
            return Response({'message': f'User with id {id} not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TableUserSerializers(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User successfully updated.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        try:
            user = TableUser.objects.get(id=id)
        except TableUser.DoesNotExist:
            return Response({'message': f'User with id {id} not found.'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'message': 'User successfully deleted.'}, status=status.HTTP_200_OK)


class TableOrderListApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        table_order = TableOrder.objects.all()
        serializer = GetTableOrderSerializers(table_order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = TableOrderSerializers(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            response_data = GetTableOrderSerializers(order)
            return Response({
                'message': 'Order successfully created.',
                'data': response_data.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TableOrderDetailApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, *args, **kwargs):
        try:
            order = TableOrder.objects.get(id=id)
        except TableOrder.DoesNotExist:
            return Response({'message': f'Order with id {id} not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GetTableOrderSerializers(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, *args, **kwargs):
        try:
            order = TableOrder.objects.get(id=id)
        except TableOrder.DoesNotExist:
            return Response({'message': f'Order with id {id} not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TableOrderSerializers(instance=order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Order successfully updated.', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, *args, **kwargs):
        try:
            order = TableOrder.objects.get(id=id)
        except TableOrder.DoesNotExist:
            return Response({'message': f'Order with id {id} not found.'}, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response({'message': 'Order successfully deleted.'}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully.',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'phone_number': user.phone_number,
                    'role': user.role,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            return Response({
                'message': 'Login successful.',
                'data': {
                    'id': data['user'].id,
                    'username': data['user'].username,
                    'email': data['user'].email,
                    'role': data['user'].role,
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Hapus token autentikasi
        request.user.auth_token.delete()
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
