from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Tag, Post, Comment
from .serializers import (
    CategorySerializer, TagSerializer,
    PostListSerializer, PostDetailSerializer,
    PostWriteSerializer, CommentSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD for categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class TagViewSet(viewsets.ModelViewSet):
    """
    CRUD for tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD for posts.
    - List returns only published posts (for public) or all for staff.
    - Detail returns full post.
    - Create/update require authentication.
    """
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'tags']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'published_at', 'title']
    ordering = ['-created_at']
    lookup_field = 'slug'

    def get_queryset(self):
        """Filter posts based on user permissions"""
        queryset = Post.objects.select_related('author', 'category').prefetch_related('tags')
        if self.request.user.is_staff:
            # Staff can see all posts
            return queryset
        # Regular users see only published posts
        return queryset.filter(status=Post.Status.PUBLISHED)

    def get_serializer_class(self):
        """Choose serializer based on action"""
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostWriteSerializer
        return PostDetailSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def comment(self, request, slug=None):
        """Add a comment to a post"""
        post = self.get_object()
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD for comments.
    - List returns only approved comments.
    - Create allows any authenticated user.
    - Update/destroy restricted to comment author or staff.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Return only approved comments for non-staff users"""
        queryset = Comment.objects.select_related('author', 'post')
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(is_approved=True)

    def perform_update(self, serializer):
        """Only author or staff can update"""
        if self.get_object().author != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        serializer.save()

    def perform_destroy(self, instance):
        """Only author or staff can delete"""
        if instance.author != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        instance.delete()