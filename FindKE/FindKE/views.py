from django.shortcuts import render
from django.db import connection
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response

def index(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
    
    context = {
        'db_version': db_version
    }
    return render(request, 'index.html', context)

class LogoutView(APIView):

    def post(self, request):
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=205)