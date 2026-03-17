"""
URL configuration for FindKE project.
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from graphene_django.views import GraphQLView
from graphql.schema import schema

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    # API endpoints
    path('api/users/', include('users.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/reminders/', include('reminders.urls')),
    path('api/posts/', include('posts.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/notifications/', include('notifications.urls')),
    # GraphQL endpoint
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema), name='graphql'),
    # Allauth URLs (for social auth)
    path('accounts/', include('allauth.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

