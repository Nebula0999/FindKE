from django.contrib.auth import authenticate
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def get(self, request):
        serializer = RegisterSerializer()
        field_config = {}

        for name, field in serializer.fields.items():
            field_config[name] = {
                'type': field.__class__.__name__,
                'required': field.required,
                'write_only': field.write_only,
                'min_length': getattr(field, 'min_length', None),
                'max_length': getattr(field, 'max_length', None),
            }

        return Response(
            {
                'message': 'Provide these fields in POST /api/users/register/.',
                'fields': field_config,
                'example': {
                    'username': 'new_user',
                    'email': 'new_user@example.com',
                    'password': 'Password123',
                    'first_name': 'First',
                    'last_name': 'Last',
                },
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user': UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        if not user:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                'token': token.key,
                'user': UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
