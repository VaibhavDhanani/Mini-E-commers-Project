from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer


@api_view(['GET'])
def order_items(request):
    if request.method == "GET":
        items = OrderItem.objects.all()
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(data = {"error": "Method not allowed"},status = status.HTTP_405_METHOD_NOT_ALLOWED)
    

@api_view(['GET', 'PUT', 'DELETE'])
def order_item(request, id):
    try:
        item = OrderItem.objects.get(id=id)
    except OrderItem.DoesNotExist:
        return Response({'error': 'Order item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = OrderItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = OrderItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(data = {"error": "Method not allowed"},status = status.HTTP_405_METHOD_NOT_ALLOWED)
        
        
@api_view(['GET', 'POST'])
def orders(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data = {"error": "Method not allowed"},status = status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT', 'DELETE'])
def order(request, id):
    try:
        order_from_db = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return Response(data={'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = OrderSerializer(order_from_db)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        if 'id' in request.data and request.data['id'] != order_from_db.id:
            return Response(
                {"error": "id in body does not match url id"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OrderSerializer(order_from_db, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        order_from_db.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(data = {"error": "Method not allowed"},status = status.HTTP_405_METHOD_NOT_ALLOWED)
