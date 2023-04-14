from rest_framework import generics, status, views, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .models import UserModel
from .serializers import UserSerializer, CreateUserSerializer, ForgotPasswordSerializer,EmailUsernameSerializer
from project.api_utils import get_response, get_error_response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken


class LoginApiView(ObtainAuthToken):
    authentication_classes = [BasicAuthentication]
    serializer_class = EmailUsernameSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        data_user = UserSerializer(user).data
        data_user['token'] = {'refresh': str(refresh), 'access': str(refresh.access_token)}
        return Response(data=data_user)


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
    authentication_classes = [JWTAuthentication]

    def get(self, request, format=None):
        user = UserModel.objects.get(pk=request.user.pk)
        return Response(data=UserSerializer(request.user).data)


class ForgotPasswordApiView(views.APIView):

    def post(self, request):

        serializer: ForgotPasswordSerializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response(data={
                "message" : "Confirmation email already sent"
            }, status=status.HTTP_200_OK)
        return Response(data={"message": "Error"}, status=status.HTTP_400_BAD_REQUEST)

class ResetPassword():
    pass
