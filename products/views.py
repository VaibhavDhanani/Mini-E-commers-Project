from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from django.db.models import Q

@api_view(['GET', 'POST'])
def products(request):
    if request.method == 'GET':
        search = request.query_params.get('search', None)
        limit = int(request.GET.get('limit',10))
        offset = int(request.GET.get('offset',0))
        
        if search:
            products = Product.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        else:
            products = Product.objects.all()[offset:offset+limit]
            
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(data = {"error": "Method not allowed"},status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
@api_view(['GET', 'PUT','DELETE'])
def product(request, id):
    try:
        product_from_db = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        product_data = ProductSerializer(product_from_db).data
        return Response(product_data,status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        if 'id' in request.data and request.data['id'] != product_from_db.id:
            return Response(
                {"error": "id in body does not match url id"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ProductSerializer(product_from_db, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        product_from_db.delete()
        return Response(data={'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(data = {"error": "Method not allowed"},status = status.HTTP_405_METHOD_NOT_ALLOWED)