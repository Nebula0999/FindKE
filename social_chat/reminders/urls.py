from django.urls import path

from .views import ReminderListCreateView, ReminderRetrieveUpdateDestroyView


urlpatterns = [
    path('', ReminderListCreateView.as_view(), name='reminder-list-create'),
    path('<int:pk>/', ReminderRetrieveUpdateDestroyView.as_view(), name='reminder-detail'),
]
