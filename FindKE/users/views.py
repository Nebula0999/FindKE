from django.contrib.auth import authenticate, get_user_model
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FriendRequest
from .serializers import (
    LoginSerializer, RegisterSerializer, UserSerializer, FriendRequestSerializer
)

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing user profiles."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        """Follow a user."""
        user_to_follow = self.get_object()
        if request.user.follow(user_to_follow):
            return Response({'status': 'following'}, status=status.HTTP_200_OK)
        return Response({'status': 'already following'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        """Unfollow a user."""
        user_to_unfollow = self.get_object()
        if request.user.unfollow(user_to_unfollow):
            return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK)
        return Response({'status': 'not following'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        """Get user's followers."""
        user = self.get_object()
        followers = user.followers.all()
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        """Get users that this user is following."""
        user = self.get_object()
        following = user.following.all()
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data)


class FriendRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for managing friend requests."""
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get friend requests for the authenticated user."""
        return FriendRequest.objects.filter(
            to_user=self.request.user
        ).select_related('from_user', 'to_user')

    def perform_create(self, serializer):
        """Create a friend request."""
        serializer.save(from_user=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Accept a friend request."""
        friend_request = self.get_object()
        friend_request.status = 'accepted'
        friend_request.save()
        # Automatically follow each other
        request.user.follow(friend_request.from_user)
        friend_request.from_user.follow(request.user)
        return Response({'status': 'accepted'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a friend request."""
        friend_request = self.get_object()
        friend_request.status = 'rejected'
        friend_request.save()
        return Response({'status': 'rejected'}, status=status.HTTP_200_OK)
