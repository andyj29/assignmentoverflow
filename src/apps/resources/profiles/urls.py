from django.urls import path
from . import views

urlpatterns = [
	path('', views.ProfileListView.as_view(), name='profiles'),
	path('<str:profile_id>', views.ProfileDetailView.as_view(), name='profile_detail')
]

