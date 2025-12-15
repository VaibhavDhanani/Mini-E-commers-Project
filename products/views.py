from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from django.db.models import Q
from utils.utils import BaseAPIView, rate_limit
from django.core.cache import cache

class ProductListCreateAPIView(BaseAPIView):
    
    @rate_limit(max_requests=10,time_window=60)
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