from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Reminder
from .serializers import ReminderSerializer


class ReminderListCreateView(generics.ListCreateAPIView):
	serializer_class = ReminderSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Reminder.objects.filter(user=self.request.user).order_by('-created_at')

	def perform_create(self, serializer):
		task = serializer.validated_data['task']
		if task.user_id != self.request.user.id:
			raise PermissionDenied('You can only create reminders for your own tasks.')
		serializer.save(user=self.request.user)


class ReminderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = ReminderSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Reminder.objects.filter(user=self.request.user)

	def perform_update(self, serializer):
		task = serializer.validated_data.get('task')
		if task and task.user_id != self.request.user.id:
			raise PermissionDenied('You can only assign reminders to your own tasks.')
		serializer.save(user=self.request.user)
