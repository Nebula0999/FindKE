"""
Main GraphQL schema for FindKE social network.
"""
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth import get_user_model
from posts.models import Post, Like, Comment
from chat.models import Conversation, Message
from notifications.models import Notification

User = get_user_model()


# Object Types
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'bio', 'avatar', 'location', 'website', 'birth_date',
            'follower_count', 'following_count', 'created_at'
        )

    follower_count = graphene.Int()
    following_count = graphene.Int()

    def resolve_follower_count(self, info):
        return self.follower_count

    def resolve_following_count(self, info):
        return self.following_count


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = (
            'id', 'user', 'content', 'image', 'is_repost',
            'original_post', 'like_count', 'comment_count',
            'repost_count', 'created_at', 'updated_at'
        )

    like_count = graphene.Int()
    comment_count = graphene.Int()
    repost_count = graphene.Int()

    def resolve_like_count(self, info):
        return self.like_count

    def resolve_comment_count(self, info):
        return self.comment_count

    def resolve_repost_count(self, info):
        return self.repost_count


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = (
            'id', 'user', 'post', 'content', 'parent_comment',
            'created_at', 'updated_at'
        )


class ConversationType(DjangoObjectType):
    class Meta:
        model = Conversation
        fields = (
            'id', 'participants', 'is_group', 'group_name',
            'group_image', 'created_at', 'updated_at'
        )


class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = (
            'id', 'conversation', 'sender', 'content', 'file',
            'file_type', 'is_edited', 'is_deleted', 'created_at'
        )


class NotificationType(DjangoObjectType):
    class Meta:
        model = Notification
        fields = (
            'id', 'recipient', 'sender', 'notification_type',
            'message', 'post', 'comment', 'conversation',
            'is_read', 'created_at'
        )


# Input Types
class RegisterInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    first_name = graphene.String()
    last_name = graphene.String()


class CreatePostInput(graphene.InputObjectType):
    content = graphene.String(required=True)
    image = graphene.String()  # Base64 encoded or URL


class SendMessageInput(graphene.InputObjectType):
    conversation_id = graphene.ID(required=True)
    content = graphene.String()
    file = graphene.String()  # Base64 encoded or URL


# Payload Types
class AuthPayload(graphene.ObjectType):
    token = graphene.String()
    user = graphene.Field(UserType)


class FollowPayload(graphene.ObjectType):
    success = graphene.Boolean()
    user = graphene.Field(UserType)


# Queries
class Query(graphene.ObjectType):
    # User queries
    me = graphene.Field(UserType)
    users = graphene.List(UserType, search=graphene.String())
    user = graphene.Field(UserType, id=graphene.ID(required=True))

    # Post queries
    feed = graphene.List(PostType, limit=graphene.Int(), offset=graphene.Int())
    post = graphene.Field(PostType, id=graphene.ID(required=True))
    user_posts = graphene.List(PostType, user_id=graphene.ID(required=True))

    # Chat queries
    conversations = graphene.List(ConversationType)
    messages = graphene.List(MessageType, conversation_id=graphene.ID(required=True))

    # Notification queries
    notifications = graphene.List(NotificationType, unread_only=graphene.Boolean())

    def resolve_me(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None

    def resolve_users(self, info, search=None):
        qs = User.objects.all()
        if search:
            qs = qs.filter(username__icontains=search) | qs.filter(email__icontains=search)
        return qs[:50]

    def resolve_user(self, info, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None

    def resolve_feed(self, info, limit=20, offset=0):
        user = info.context.user
        if not user.is_authenticated:
            return []

        # Get posts from followed users and own posts
        following_ids = user.following.values_list('id', flat=True)
        return Post.objects.filter(
            user_id__in=list(following_ids) + [user.id]
        ).select_related('user').order_by('-created_at')[offset:offset+limit]

    def resolve_post(self, info, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return None

    def resolve_user_posts(self, info, user_id):
        return Post.objects.filter(user_id=user_id).order_by('-created_at')

    def resolve_conversations(self, info):
        user = info.context.user
        if not user.is_authenticated:
            return []
        return user.conversations.all()

    def resolve_messages(self, info, conversation_id):
        user = info.context.user
        if not user.is_authenticated:
            return []
        try:
            conversation = Conversation.objects.get(pk=conversation_id)
            if user in conversation.participants.all():
                return conversation.messages.all()
        except Conversation.DoesNotExist:
            pass
        return []

    def resolve_notifications(self, info, unread_only=False):
        user = info.context.user
        if not user.is_authenticated:
            return []
        qs = user.notifications.all()
        if unread_only:
            qs = qs.filter(is_read=False)
        return qs


# Mutations
class Register(graphene.Mutation):
    class Arguments:
        input = RegisterInput(required=True)

    Output = AuthPayload

    def mutate(self, info, input):
        from rest_framework.authtoken.models import Token

        user = User.objects.create_user(
            username=input.username,
            email=input.email,
            password=input.password,
            first_name=input.get('first_name', ''),
            last_name=input.get('last_name', '')
        )
        token, _ = Token.objects.get_or_create(user=user)
        return AuthPayload(token=token.key, user=user)


class Login(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    Output = AuthPayload

    def mutate(self, info, email, password):
        from django.contrib.auth import authenticate
        from rest_framework.authtoken.models import Token

        # Try to authenticate with email
        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return AuthPayload(token=token.key, user=user)
        return None


class CreatePost(graphene.Mutation):
    class Arguments:
        input = CreatePostInput(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, input):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Authentication required')

        post = Post.objects.create(
            user=user,
            content=input.content
        )
        return CreatePost(post=post)


class FollowUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    Output = FollowPayload

    def mutate(self, info, user_id):
        current_user = info.context.user
        if not current_user.is_authenticated:
            raise Exception('Authentication required')

        try:
            user_to_follow = User.objects.get(pk=user_id)
            success = current_user.follow(user_to_follow)
            return FollowPayload(success=success, user=user_to_follow)
        except User.DoesNotExist:
            return FollowPayload(success=False, user=None)


class UnfollowUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    Output = FollowPayload

    def mutate(self, info, user_id):
        current_user = info.context.user
        if not current_user.is_authenticated:
            raise Exception('Authentication required')

        try:
            user_to_unfollow = User.objects.get(pk=user_id)
            success = current_user.unfollow(user_to_unfollow)
            return FollowPayload(success=success, user=user_to_unfollow)
        except User.DoesNotExist:
            return FollowPayload(success=False, user=None)


class SendMessage(graphene.Mutation):
    class Arguments:
        input = SendMessageInput(required=True)

    message = graphene.Field(MessageType)

    def mutate(self, info, input):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Authentication required')

        try:
            conversation = Conversation.objects.get(pk=input.conversation_id)
            if user not in conversation.participants.all():
                raise Exception('Not a participant in this conversation')

            message = Message.objects.create(
                conversation=conversation,
                sender=user,
                content=input.get('content', '')
            )
            return SendMessage(message=message)
        except Conversation.DoesNotExist:
            raise Exception('Conversation not found')


class MarkMessageRead(graphene.Mutation):
    class Arguments:
        message_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, message_id):
        user = info.context.user
        if not user.is_authenticated:
            return MarkMessageRead(success=False)

        try:
            from chat.models import MessageReadReceipt
            message = Message.objects.get(pk=message_id)
            MessageReadReceipt.objects.get_or_create(message=message, user=user)
            return MarkMessageRead(success=True)
        except Message.DoesNotExist:
            return MarkMessageRead(success=False)


class Mutation(graphene.ObjectType):
    register = Register.Field()
    login = Login.Field()
    create_post = CreatePost.Field()
    follow_user = FollowUser.Field()
    unfollow_user = UnfollowUser.Field()
    send_message = SendMessage.Field()
    mark_message_read = MarkMessageRead.Field()


# Subscriptions (placeholder - requires additional setup with channels-graphql-ws)
class Subscription(graphene.ObjectType):
    message_sent = graphene.Field(MessageType, conversation_id=graphene.ID(required=True))
    new_notification = graphene.Field(NotificationType)


# Schema
schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
