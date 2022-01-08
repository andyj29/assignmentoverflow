from rest_framework import permissions, generics
from django.shortcuts import get_object_or_404
from .serializers import ProfileSerializer
from .models import Profile
from .permissions import IsAuthorizedOrReadOnly


class ProfileListView(generics.ListAPIView):
	serializer_class = ProfileSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def get_queryset(self):
		return Profile.objects.all()


class ProfileDetailView(generics.RetrieveUpdateAPIView):
	serializer_class = ProfileSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorizedOrReadOnly)

	def get_object(self):
		profile = get_object_or_404(Profile, pk=self.kwargs['profile_id'])
		self.check_object_permissions(self.request, profile)
		return profile