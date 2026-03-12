from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Tag, Post, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'created_at']
        read_only_fields = ['slug', 'created_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at']
        read_only_fields = ['slug', 'created_at']


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for list view (lighter)"""
    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'author',
            'category', 'tags', 'status', 'published_at',
            'created_at'
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for detail view (full content)"""
    author = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt',
            'featured_image', 'author', 'category', 'tags',
            'status', 'published_at', 'created_at', 'updated_at',
            'comments'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at', 'published_at']

    def get_comments(self, obj):
        """Return only approved comments"""
        comments = obj.comments.filter(is_approved=True)
        return CommentSerializer(comments, many=True).data


class PostWriteSerializer(serializers.ModelSerializer):
    """Serializer for create/update operations"""
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'excerpt', 'featured_image',
            'category', 'tags', 'status'
        ]

    def create(self, validated_data):
        # Automatically set author to current user
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'is_approved', 'created_at']
        read_only_fields = ['author', 'is_approved', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)