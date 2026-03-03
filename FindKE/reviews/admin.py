from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'reviewer', 'reviewee', 'rating')
    search_fields = ('reviewer__name', 'reviewee__name', 'job__title')
    list_filter = ('rating',)
