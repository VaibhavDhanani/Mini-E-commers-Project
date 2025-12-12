from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from django.db.models import Q
import redis
from utils.utils import BaseAPIView
import requests
from django.core.cache import cache

class ProductListCreateAPIView(BaseAPIView):
    def get(self,request):
        search = request.query_params.get('search', None)
        limit = int(request.GET.get('limit',1000))
        offset = int(request.GET.get('offset',0))
        
        if search:
            cache_key = f"search:{search}"
        else:
            cache_key = f"products:{offset}:{limit}"
            
        cached_data = cache.get(cache_key)
        if cached_data:
            return self.success_response(cached_data)
            
        if search:
            products = Product.objects.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        else:
            products = Product.objects.all()[offset:offset+limit]
            
        serializer = ProductSerializer(products, many=True)
        cache.set(cache_key,serializer.data)
        
        return self.success_response(serializer.data)
    
    def post(self,request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.success_response(data=serializer.data,status_code =status.HTTP_201_CREATED)
        return self.failure_response(data=serializer.errors)
    
  
        response = requests.get('https://dummyjson.com/products?limit=194')
        data = response.json()            # convert API response to Python dict
        products = data.get('products', [])
        count=0
        for product in products:
            new_product = {
                "name": product.get("title"),        # dummyjson uses "title", not "name"
                "description": product.get("description"),
                "price": product.get("price")
            }

            serializer = ProductSerializer(data=new_product)

            if serializer.is_valid():
                serializer.save()
                count+=1
            else:
                print(serializer.errors)  # optional: log errors

        return Response({"message": f"Products {count} added successfully!"})

            
        
    
class ProductDetailAPIView(BaseAPIView):
    
    def get_product(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return self.failure_response(message=f"product with {id} not found",status_code=status.HTTP_404_NOT_FOUND)
    
    def get(self,request,id):
        product = self.get_product(id)
        serializer = ProductSerializer(product)
        return self.success_response(data=serializer.data)
    
    
    def put(self,request,id):
        product = self.get_product(id)
        if 'id' in request.data and request.data['id'] != product.id:
            return self.failure_response(
                message="id in body does not match url id", 
            )
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.success_response(serializer.data,status_code=status.HTTP_204_NO_CONTENT)
        return self.failure_response(data=serializer.errors)
    
    def delete(self,request,id):
        product = self.get_product(id)
        product.delete()
        return self.success_response(message='Product deleted successfully', status_code=status.HTTP_204_NO_CONTENT)