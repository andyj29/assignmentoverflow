from django.urls import path
from . import views


urlpatterns = [
	path('', views.PostListView.as_view(), name='posts'),
	path('me/', views.CurrentUserPostListView.as_view(), name='my_posts'),
	path('<str:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
	path('<str:post_id>/comments/', views.CommentListView.as_view(), name='comments'),
	path('<str:post_id>/comments/<str:comment_id>/', views.CommentDetailView.as_view(), name='comment_detail'),
]