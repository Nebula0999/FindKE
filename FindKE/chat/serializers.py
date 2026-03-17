from rest_framework import serializers
from .models import Conversation, Message, MessageReadReceipt
from users.serializers import UserSerializer


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'id', 'participants', 'is_group', 'group_name',
            'group_image', 'last_message', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        last_msg = obj.last_message
        if last_msg:
            return MessageSerializer(last_msg).data
        return None


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id', 'conversation', 'sender', 'content', 'file',
            'file_type', 'is_edited', 'is_deleted', 'is_read',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'sender', 'created_at', 'updated_at']

    def get_is_read(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.read_receipts.filter(user=request.user).exists()
        return False


class MessageReadReceiptSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = MessageReadReceipt
        fields = ['id', 'message', 'user', 'read_at']
        read_only_fields = ['id', 'user', 'read_at']
