from rest_framework import permissions, generics, filters
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import RegistrationSerializer, UserSerializer
from .permissions import IsAuthorizedOrReadOnly


class RegistrationView(generics.CreateAPIView):
	permission_classes = (permissions.AllowAny,)
	serializer_class = RegistrationSerializer


class UserListView(generics.ListAPIView):
	permission_classes = (permissions.IsAdminUser,)
	serializer_class = UserSerializer

	def get_queryset(self):
		return User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticated, IsAuthorizedOrReadOnly)
	serializer_class = UserSerializer

	def get_object(self):
		user = get_object_or_404(User, pk=self.kwargs['user_id'])
		self.check_object_permissions(self.request, user)
		return user
