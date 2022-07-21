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
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        data_user = UserSerializer(user).data
        data_user['token'] = token.key

        return get_response(message='Success', code=0, data=data_user)


class RegisterApiView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        response = super(RegisterApiView, self).post(request, *args, **kwargs)
        return get_response(data=response.data)


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
