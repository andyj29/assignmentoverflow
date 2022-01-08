from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
	name = 'src.apps.authentication'

	def ready(self):
		import src.apps.authentication.signals