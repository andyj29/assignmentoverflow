from django.urls import path
from . import views


urlpatterns = [
	path('', views.ChatSessionListView.as_view(), name='chat'),
	path('<uuid:session_id>/', views.ChatSessionDetailView.as_view(), name='chat_session_detail')

]