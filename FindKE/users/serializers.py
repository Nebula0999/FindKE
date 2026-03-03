from rest_framework.serializers import ModelSerializer
from . models import User, Client, Freelancer, Admin



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'name', 'email', 'role', 'skills', 'rating']


class AdminSerializer(ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'user']

class ClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'company_name', 'job_success_rate', 'spending']

class FreelancerSerializer(ModelSerializer):
    class Meta:
        model = Freelancer
        fields = ['id', 'user', 'portfolio', 'job_applications', 'job_success_rate', 'earnings']