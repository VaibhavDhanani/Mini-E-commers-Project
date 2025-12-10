from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

def list_order_items(request):
    items = OrderItem.objects.all()
    serializer = OrderItemSerializer(items, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def order_items(request):
    actions = {
        'GET': list_order_items,
    }
    return actions[request.method](request)


def get_order_item(request, id):
    try:
        item = OrderItem.objects.get(id=id)
        serializer = OrderItemSerializer(item)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except OrderItem.DoesNotExist:
        return Response(data={'error': 'Order item not found'}, status=status.HTTP_404_NOT_FOUND)


def update_order_item(request, id):
    try:
        item = OrderItem.objects.get(id=id)
        serializer = OrderItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except OrderItem.DoesNotExist:
        return Response(data={'error': 'Order item not found'}, status=status.HTTP_404_NOT_FOUND)


def delete_order_item(request, id):
    try:
        item = OrderItem.objects.get(id=id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except OrderItem.DoesNotExist:
        return Response(data={'error': 'Order item not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', 'DELETE'])
def order_item(request, id):
    actions = {
        'GET': get_order_item,
        'PUT': update_order_item,
        'DELETE': delete_order_item,
    }
    return actions[request.method](request, id)


def list_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def orders(request):
    actions = {
        'GET': list_orders,
        'POST': create_order,
    }
    return actions[request.method](request)


def get_order(request, id):
    try:
        order_from_db = Order.objects.get(id=id)
        serializer = OrderSerializer(order_from_db)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response(data={'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


def update_order(request, id):
    try:
        order_from_db = Order.objects.get(id=id)
        if 'id' in request.data and request.data['id'] != order_from_db.id:
            return Response(
                data={"error": "id in body does not match url id"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = OrderSerializer(order_from_db, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Order.DoesNotExist:
        return Response(data={'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


def delete_order(request, id):
    try:
        order_from_db = Order.objects.get(id=id)
        order_from_db.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Order.DoesNotExist:
        return Response(data={'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT', 'DELETE'])
def order(request, id):
    actions = {
        'GET': get_order,
        'PUT': update_order,
        'DELETE': delete_order,
    }
    return actions[request.method](request, id)
