from django.urls import path, include


urlpatterns = [
	path('profiles/', include(('src.apps.resources.profiles.urls', 'profiles'))),
]