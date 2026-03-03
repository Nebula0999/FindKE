from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'jobs', views.JobPostingViewSet)
router.register(r'jobapplications', views.JobApplicationViewSet)
router.register(r'jobassignments', views.JobAssignmentViewSet)
router.register(r'jobcompletions', views.JobCompletionViewSet)
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]