from django.contrib import admin
from .models import User, Client, Freelancer, Admin

admin.site.register(User)
admin.site.register(Client) 
admin.site.register(Freelancer)
admin.site.register(Admin)

# Register your models here.
