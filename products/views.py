from django.core.cache import cache
from django.db.models import Q, Case, When
from rest_framework import status

from utils.utils import BaseAPIView, rate_limit

from .documents import ProductDocument, log_search
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateAPIView(BaseAPIView):
    
    def search_products(self, query, offset=0, limit=10):
        search = ProductDocument.search()
        search = search.query(
            "bool",
            should=[
                {
                    "match": {
                        "name": {
                            "query": query,
                            "fuzziness": "AUTO",
                            "boost": 3
                        }
                    }
                },
                {
                    "match": {
                        "description": {
                            "query": query,
                            "fuzziness": "AUTO",
                            "boost": 1
                        }
                    }
                }
            ],
            minimum_should_match=1
        )

        search = search[offset:offset + limit]

        response = search.execute()
        hits = response.hits
        ids = [int(hit.meta.id) for hit in hits]
        
        if not ids:
            return Product.objects.none()
        preserved_order = Case(
            *[When(id=pk, then=pos) for pos, pk in enumerate(ids)]
        )
        products=Product.objects.filter(id__in=ids).order_by(preserved_order)
        log_search(query,products)
        return products

    
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
            products = self.search_products(search)
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