from django.urls import path, include


urlpatterns = [
	path('auth/', include(('src.apps.authentication.urls', 'auth'))),
	path('resources/', include(('src.apps.resources.urls', 'resources'))),
	path('chat/', include(('src.apps.websocketchat.urls', 'chat'))),
	path('network/', include(('src.apps.networking.urls', 'network'))),
]