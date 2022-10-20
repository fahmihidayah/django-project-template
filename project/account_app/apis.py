from rest_framework import generics, status, views, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserModel
from .serializers import UserSerializer, CreateUserSerializer
from project.api_utils import get_response, get_error_response
from rest_framework.authtoken.models import Token


class LoginApiView(ObtainAuthToken):
    authentication_classes = [BasicAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data_user = UserSerializer(user).data
            data_user['token'] = token.key
            return Response(
                data={
                    "message": "Success Login",
                    "code": status.HTTP_200_OK,
                    "error": False,
                    "details": data_user
                }
            )
        else:
            return Response(
                data={
                    "message": "Error Login",
                    "code": status.HTTP_400_BAD_REQUEST,
                    "error": False,
                    "details": None
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class RegisterApiView(generics.CreateAPIView):
    authentication_classes = []
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.create(serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LogoutApiView(views.APIView):

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return get_response()

class UserDetailApiView(views.APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):
        return get_response(data={
            'user': UserSerializer(request.user).data
        })


class ForgotApiPassword():
    pass


class ResetPassword():
    pass
