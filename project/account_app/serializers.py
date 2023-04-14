from rest_framework import serializers
from .models import ModelBackend, UserModel
from django.contrib.auth import authenticate


class EmailUsernameSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    username: serializers.CharField = serializers.CharField(required=False)
    email: serializers.EmailField = serializers.EmailField(required=False)
    password: serializers.CharField = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')

        if not email and not username:
            msg = 'Must include username or email and password.'
            raise serializers.ValidationError(msg, code='authorization')
        elif username and password:

            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        elif email and password:
            user = UserModel.objects.get(email=email)
            user = authenticate(request=self.context.get('request'), username=user.username, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include username and password.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def is_valid(self, raise_exception=False):
        valid = super(ForgotPasswordSerializer, self).is_valid()

        if valid and  UserModel.objects.filter(email=self.validated_data['email']).count() == 0:
            raise serializers.ValidationError({
                "email": "No email found"
            })
        return valid


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()


class CreateUserSerializer(serializers.Serializer):
    pk = serializers.IntegerField(required=False, read_only=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def is_valid(self, raise_exception=False):
        valid = super(CreateUserSerializer, self).is_valid()
        if UserModel.objects.filter(email=self.initial_data['email']).count() != 0 and valid:
            raise serializers.ValidationError({"email": "email already used"})
        if not valid:
            raise serializers.ValidationError(self.errors)

        return valid

    def create(self, validated_data):
        return UserModel.objects.create_user(email=validated_data['email'], username=validated_data['email'],
                                             password=validated_data['password'],
                                             first_name=validated_data['first_name'],
                                             last_name=validated_data['last_name'])
