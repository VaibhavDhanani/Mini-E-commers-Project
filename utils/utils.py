from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

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
