from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer, LikeSerializer


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for managing posts."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter posts based on user authentication."""
        return Post.objects.annotate(
            like_count=Count('likes'),
            comment_count=Count('comments'),
            repost_count=Count('reposts')
        ).select_related('user').order_by('-created_at')

    def perform_create(self, serializer):
        """Set the user when creating a post."""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def feed(self, request):
        """Get personalized feed for the authenticated user."""
        user = request.user
        following_ids = user.following.values_list('id', flat=True)
        posts = self.get_queryset().filter(
            user_id__in=list(following_ids) + [user.id]
        )
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Like a post."""
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'already liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """Unlike a post."""
        post = self.get_object()
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'status': 'not liked'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def repost(self, request, pk=None):
        """Repost a post."""
        original_post = self.get_object()
        repost = Post.objects.create(
            user=request.user,
            content=request.data.get('content', ''),
            is_repost=True,
            original_post=original_post
        )
        serializer = self.get_serializer(repost)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing comments."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Optionally filter comments by post."""
        queryset = Comment.objects.select_related('user', 'post')
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        """Set the user when creating a comment."""
        serializer.save(user=self.request.user)
