from rest_framework.response import Response
from rest_framework import generics, status, views, viewsets

def map_data_response(message : str = 'Request success',
                 code: int = 0,
                 data = None) -> dict:
    return {
        'message' : message,
        'code' : code,
        'details': data,
    }


def get_response(message : str = 'Request success',
                 code: int = 0,
                 data= None) -> Response:
    return Response(data=map_data_response(message, code, data))


def get_error_response(message : str = 'Request success',
                 code: int = 0,
                 data= None) -> Response:
    return Response(data=map_data_response(message, code, data), status=status.HTTP_401_UNAUTHORIZED)
