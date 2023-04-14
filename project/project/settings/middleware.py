import json

import jsonpickle
from django.http import HttpRequest, HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.renderers import JSONRenderer


def get_message_error(error_data: dict) -> str:
    message = ""
    for key in error_data:
        error = error_data[key]
        if error is not list:
            message = error.title()
        else:
            message = error[0].title()
        break
    return message


class RestAPIFormatMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if 'api' in request.path:
            response: Response = self.get_response(request)
            if response.status_code >= status.HTTP_200_OK \
                    | response.status_code <= status.HTTP_208_ALREADY_REPORTED:
                response.data = {
                    "message": "Success Request",
                    "error": False,
                    "code": response.status_code,
                    "details": response.data
                }
                response._is_rendered = False
                response.render()
                return response
            if response.status_code == status.HTTP_400_BAD_REQUEST:
                list_error_message = []
                for key, values in response.data.items():
                    list_error_message.extend([f"{key} {value}" for value in values])

                response.content = jsonpickle.encode({
                    "message": "Bad Request",
                    "error": True,
                    "code": response.status_code,
                    "error_details": list_error_message
                })
                return response
            if response.status_code == status.HTTP_401_UNAUTHORIZED:
                response.data = {
                    "message": "Authentication credentials were not provided.",
                    "error": True,
                    "code": response.status_code,
                    "details": None 
                }
                response._is_rendered = False
                response.render()
                return response
            if response.status_code == status.HTTP_403_FORBIDDEN:
                response.content = jsonpickle.encode({
                    "message": "Forbidden",
                    "error": True,
                    "code": response.status_code,
                    "details": None
                })
                return response
            if response.status_code == status.HTTP_404_NOT_FOUND:
                response.content = jsonpickle.encode({
                    "message": "Not Found",
                    "error": True,
                    "code": response.status_code,
                    "details": None
                })
                return response
            if response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
                response.content = jsonpickle.encode({
                    "message": "Method Not Allowed",
                    "error": True,
                    "code": response.status_code,
                    "details": None
                })
                return response
            if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
                response.content = jsonpickle.encode({
                    "message": "Internal server error",
                    "error": True,
                    "code": response.status_code,
                    "details": None
                })
                return response
            return response

        else:
            return self.get_response(request)