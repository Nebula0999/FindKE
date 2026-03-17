from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Conversation, Message, MessageReadReceipt
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing conversations."""
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get conversations for the authenticated user."""
        return Conversation.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants').order_by('-updated_at')

    @action(detail=False, methods=['post'])
    def create_or_get(self, request):
        """Create a new conversation or get existing one."""
        participant_ids = request.data.get('participant_ids', [])
        is_group = request.data.get('is_group', False)

        if not participant_ids:
            return Response(
                {'error': 'At least one participant required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # For 1-on-1 chats, check if conversation already exists
        if not is_group and len(participant_ids) == 1:
            existing = Conversation.objects.filter(
                is_group=False,
                participants=request.user
            ).filter(
                participants__id=participant_ids[0]
            ).first()

            if existing:
                serializer = self.get_serializer(existing)
                return Response(serializer.data)

        # Create new conversation
        conversation = Conversation.objects.create(
            is_group=is_group,
            group_name=request.data.get('group_name', '') if is_group else ''
        )
        conversation.participants.add(request.user)
        for participant_id in participant_ids:
            conversation.participants.add(participant_id)

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing messages."""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get messages for conversations the user is part of."""
        user_conversations = Conversation.objects.filter(participants=self.request.user)
        queryset = Message.objects.filter(
            conversation__in=user_conversations
        ).select_related('sender', 'conversation')

        # Filter by conversation if provided
        conversation_id = self.request.query_params.get('conversation', None)
        if conversation_id:
            queryset = queryset.filter(conversation_id=conversation_id)

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        """Set the sender when creating a message."""
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a message as read."""
        message = self.get_object()
        receipt, created = MessageReadReceipt.objects.get_or_create(
            message=message,
            user=request.user
        )
        return Response({'status': 'marked as read'}, status=status.HTTP_200_OK)
