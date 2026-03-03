from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users-view', views.UserViewSet)
router.register(r'clients', views.ClientViewSet)
router.register(r'freelancers', views.FreelancerViewSet)
router.register(r'admins', views.AdminViewSet)

urlpatterns = [
    path('', include(router.urls)),
]