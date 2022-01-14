from django.contrib import admin
from .models import Network, ConnectRequest, ConnectNotification


admin.site.register(Network)
admin.site.register(ConnectRequest)
admin.site.register(ConnectNotification)