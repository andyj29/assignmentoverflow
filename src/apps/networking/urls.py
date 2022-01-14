from django.urls import path
from . import views


urlpatterns = [
	path('me/', views.MyNetworkDetailView.as_view(), name='my_network'),
	path('<str:network_id>/', views.NetworkDetailView.as_view(), name='network_detail'),
	path('me/requests/', views.MyConnectRequestListCreateView.as_view(), name='my_requests'),
	path('me/invites/', views.MyConnectInviteListAcceptView.as_view(), name='my_invites'),
]