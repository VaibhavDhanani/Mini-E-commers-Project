from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer


@api_view(['GET', 'POST'])
def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data = {"error": "Method not allowed"},status = status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT', 'DELETE'])
def user(request, id):
    try:
        user_from_db = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(data={'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user_from_db)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        if 'id' in request.data and request.data['id'] != user_from_db.id:
            return Response(
                {"error": "id in body does not match url id"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSerializer(user_from_db, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user_from_db.delete()
        return Response(data={'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(data = {"error": "Method not allowed"},status = status.HTTP_405_METHOD_NOT_ALLOWED)