import redis
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import Throttled

class APIViewresponseMixin:
    SUCCESS="success"
    FAILURE="failure"
    
    @classmethod
    def success_response(cls,data=None,message=None,status_code=status.HTTP_200_OK):
        """Returns Success response

        Args:
            data (Object, optional): data to be sent to client. Defaults to None.
            message (str, optional): success message if there. Defaults to None.
            status_code (int, optional): status code according to response. Defaults to status.HTTP_200_OK.
        """
        response_data = {
          "status_code": status_code,
          "status": cls.SUCCESS
        }
        if message is not None:
            response_data["message"] = message
        if data is not None:
            response_data["data"] = data
        return Response(response_data, status=status_code)
    
    @classmethod
    def failure_response(cls, data=None, message=None, status_code=status.HTTP_400_BAD_REQUEST):
        """
        Returns Failure Response
        
        Args:
            data (Object, optional): data to be sent to client. Defaults to None.
            message (str, optional): success message if there. Defaults to None.
            status_code (int, optional): status code according to response. Defaults to status.HTTP_200_OK.
        """
        response_data = {
          "status_code": status_code,
          "status": cls.FAILURE
        }
        if message is not None:
            response_data["message"] = message
        if data is not None:
            response_data["data"] = data
        return Response(response_data, status=status_code)
    
    
class BaseAPIView(APIView,APIViewresponseMixin):
    """
    Create a base API view that combines APIView and APIViewResponseMixin
    Custom API View to handle all the common logic for all APIs
    """
    pass



redis_client=redis.StrictRedis(host="localhost",port=6379,db=0,decode_responses=True)

def rate_limit(max_requests:int=5,time_window:int=60*5):
    """
    rate limiting 

    Args:
        max_requests (int, optional): Max number of requests user can in time window.. Defaults to 5.
        time_window (int, optional): A fixed time window.. Defaults to 60*5.
    """
    
    def decorator(func):
        def wrapper(self,request,*args, **kwargs):
            client_id = request.META.get('REMOTE_ADDR')
            endpoint = request.path
            redis_key = f"rate_limit:{client_id}:{endpoint}"
            
            current_requests = redis_client.get(redis_key)
            
            if current_requests is None:
                redis_client.set(redis_key,1,ex=time_window)
            elif int(current_requests) < max_requests:
                redis_client.incr(redis_key)
            else:
                retry_after = redis_client.ttl(redis_key)
                raise Throttled(detail=f"Rate limit exceed for client: {client_id}, Try again after: {retry_after} seconds")
            return func(self,request,*args,**kwargs)
        return wrapper
    return decorator

            
            
             