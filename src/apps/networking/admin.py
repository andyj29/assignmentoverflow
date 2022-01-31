from django.contrib import admin
from .models import Network, ConnectRequest


admin.site.register(Network)
admin.site.register(ConnectRequest)