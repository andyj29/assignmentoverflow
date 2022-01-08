from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
	self = serializers.HyperlinkedIdentityField(view_name='v1:resources:profiles:profile_detail', lookup_url_kwarg='profile_id')

	class Meta:
		model = Profile
		exclude = ('id', 'user')