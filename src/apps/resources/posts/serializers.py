from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Post, Comment, Tag


class CommentHyperlink(serializers.HyperlinkedRelatedField):
	view_name = 'v1:resources:posts:comment_detail'

	def get_url(self, obj, view_name, request, format):
		url_kwargs = {
			'post_id': obj.post.id,
			'comment_id': obj.id
		}

		return reverse(view_name, kwargs=url_kwargs, request=request, format=format)


class PostSerializer(serializers.ModelSerializer):
	self = serializers.HyperlinkedIdentityField(view_name='v1:resources:posts:post_detail', lookup_url_kwarg='post_id')
	author = serializers.HyperlinkedRelatedField(view_name='v1:auth:user_detail', read_only=True, lookup_url_kwarg='user_id')
	num_of_comments = serializers.SerializerMethodField()
	comments = CommentHyperlink(many=True, read_only=True)

	class Meta:
		model = Post
		fields = ('self', 'author', 'title', 'content', 'num_of_comments', 'tags', 'comments', 'last_modified', 'created')

	def get_num_of_comments(self, obj):
		return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):

	class Meta:
		model = Comment
		fields = ('__all__')

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = ('__all__')

