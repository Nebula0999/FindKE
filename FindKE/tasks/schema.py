import graphene
from graphene_django import DjangoObjectType
from .models import Task

class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = "__all__"

class Query(graphene.ObjectType):
    all_tasks = graphene.List(TaskType)

    def resolve_all_tasks(root, info):
        user = info.context.user
        if user.is_anonymous:
            return Task.objects.none()
        return Task.objects.filter(user=user).order_by('-created_at')
    
schema = graphene.Schema(query=Query)