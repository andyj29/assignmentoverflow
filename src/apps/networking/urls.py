from django.urls import path
from . import views


urlpatterns = [
	path('me/', views.MyNetworkDetailView.as_view(), name='my_network'),
	path('me/requests/', views.MyConnectRequestListView.as_view(), name='my_requests'),
	path('me/invites/', views.MyConnectInviteListView.as_view(), name='my_invites'),
	path('send/<str:receiver_username>/', views.SendRequestView.as_view(), name='send_request'),
	path('accept/<str:sender_username>/', views.AcceptRequestView.as_view(), name='accept_request'),
]