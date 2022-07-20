from django.urls import path
from . import views


urlpatterns = [
	path('me/', views.MyNetworkDetailView.as_view(), name='my_network'),
	path('<uuid:network_id>/', views.NetworkDetailView.as_view(), name='network_detail'),
	path('requests/', views.MyConnectRequestListCreateView.as_view(), name='my_requests'),
	path('invites/', views.MyConnectInviteListAcceptDeclineView.as_view(), name='my_invites'),
]