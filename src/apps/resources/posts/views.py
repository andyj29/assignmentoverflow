from rest_framework import permissions, generics, filters
from django.shortcuts import get_object_or_404
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment
from .permissions import IsAuthorizedOrReadOnly


class PostListView(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	serializer_class = PostSerializer
	search_fields = ['author_username', 'author_email', 'title', 'content', 'tags_name']
	filter_backends = (filters.SearchFilter,)

	def get_queryset(self):
		return Post.objects.all()

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)


class CurrentUserPostListView(generics.ListAPIView):
	serializer_class = PostSerializer
	search_fields = ['title', 'content', 'tags_name']
	filter_backends = (filters.SearchFilter,)

	def get_queryset(self):
		return Post.objects.filter(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorizedOrReadOnly)
	serializer_class = PostSerializer

	def get_object(self):
		post = get_object_or_404(Post, pk=self.kwargs['post_id'])
		self.check_object_permissions(self.request, post)
		return post


class CommentListView(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	serializer_class = CommentSerializer

	def get_queryset(self):
		post = get_object_or_404(Post, pk=self.kwargs['post_id'])
		return post.comments.all()

	def perform_create(self, serializer):
		serializer.save(author=self.request.user, post=get_object_or_404(Post, pk=self.kwargs['post_id']))


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorizedOrReadOnly)
	serializer_class = CommentSerializer

	def get_object(self):
		comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
		return comment




