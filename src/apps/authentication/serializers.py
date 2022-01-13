from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
	self = serializers.HyperlinkedIdentityField(view_name='v1:auth:user_detail', lookup_url_kwarg='user_id')
	profile = serializers.HyperlinkedRelatedField(view_name='v1:resources:profiles:profile_detail', read_only=True, lookup_url_kwarg='profile_id')
	network = serializers.HyperlinkedRelatedField(view_name='v1:networking:network_detail', read_only=True, lookup_url_kwarg='network_id')

	class Meta:
		model = User
		fields = ('self', 'username', 'email', 'profile')


class RegistrationSerializer(serializers.ModelSerializer):
	username = serializers.CharField(max_length=128, required=True, validators=[UniqueValidator(queryset=User.objects.all())])
	email = serializers.EmailField(max_length=255, required=True, validators=[UniqueValidator(queryset=User.objects.all())])
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = password2 = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = User
		fields = ('username', 'email', 'password', 'password2')

	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError({'password': 'Password doesn\'t match.'})

		return attrs

	def create(self, validated_data):
		user = User.objects.create(username=validated_data['username'], email=validated_data['email'])

		user.set_password(validated_data['password'])
		user.save()

		return user
