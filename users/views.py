from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer


class UserView(APIView):
    def get(self,request,user_id=None):
        if user_id:
            try:
                user_from_db = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response(data={'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(user_from_db)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,user_id):
        try:
            user_from_db = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(data={'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if 'user_id' in request.data and request.data['user_id'] != user_from_db.id:
            return Response(
                {"error": "id in body does not match url id"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSerializer(user_from_db, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,user_id):
        try:
            user_from_db = User.objects.get(id=user_id)
            user_from_db.delete()
            return Response(data={'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(data={'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

