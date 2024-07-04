"""
Views for recipe API
"""
from rest_framework import (
    viewsets,
    mixins
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag
)
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""

    # By default we want to use detail serializer
    # because we need it for Create, Update and Delete
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # We want to filter the queryset by authenticated user
    def get_queryset(self):
        """Retreive recipes for authenticated user"""
        return self.queryset.filter(
            user=self.request.user
        ).order_by(
            '-id'
        )

    def get_serializer_class(self):
        """Return the serializer class per request"""

        # But if we want to list the items
        # we use the normal serializer
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""

        serializer.save(user=self.request.user)


class TagViewset(
            mixins.DestroyModelMixin,
            mixins.UpdateModelMixin,
            mixins.ListModelMixin,
            viewsets.GenericViewSet):
    """View for managing tags API"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user"""
        return self.queryset.filter(
            user=self.request.user
        ).order_by(
            '-name'
        )
