from django.urls import path, include


urlpatterns = [
	path('auth/', include(('src.apps.authentication.urls', 'auth'))),
	path('resources/', include(('src.apps.resources.urls', 'resources'))),
]