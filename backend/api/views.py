from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api import paginators, permissions, serializers, filters
from recipes.models import Favorite, Ingredient, Recipe, Tag, ShoppingCart
from users.models import Subscription

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = paginators.LimitedPagePagination

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, **kwargs):
        author = get_object_or_404(User, id=kwargs.get('id'))
        if request.method == 'POST':
            Subscription.objects.create(
                user=request.user, author=author)
            serializer = serializers.SubscriptionSerializer(
                author, data=request.data, context={'request': request})
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        subscription = get_object_or_404(
            Subscription, user=request.user, author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribing__user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = serializers.SubscriptionSerializer(
            pages, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_backends = (filters.IngredientFilter,)
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.select_related('author')
    serializer_class = serializers.RecipeSerializer
    permission_classes = (permissions.IsAuthorOrStaffOrReadOnly,)
    pagination_class = paginators.LimitedPagePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.RecipeFilter

    @action(detail=True, permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        ...

    @favorite.mapping.post
    def recipe_to_favorites(self, request, pk):
        return self._add_recipe(Favorite, request, pk)

    @favorite.mapping.delete
    def remove_recipe_from_favorites(self, request, pk):
        return self._remove_recipe(Favorite, request, pk)

    @action(detail=True, permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        ...

    @shopping_cart.mapping.post
    def recipe_to_cart(self, request, pk):
        return self._add_recipe(ShoppingCart, request, pk)

    @shopping_cart.mapping.delete
    def remove_recipe_from_cart(self, request, pk):
        return self._remove_recipe(ShoppingCart, request, pk)

    def _remove_recipe(self, model, request, pk):
        obj = model.objects.filter(recipe__id=pk, user=request.user).first()
        if not obj:
            return Response({'error': f'{model.__name__} не существует!'},
                            status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status.HTTP_204_NO_CONTENT)

    def _add_recipe(self, model, request, pk):
        recipe = get_object_or_404(self.queryset, pk=pk)
        try:
            model(recipe=recipe, user=request.user).save()
        except IntegrityError:
            return Response({'error': f'{model.__name__} уже существует!'})
        return Response(serializers.ShortRecipeSerializer(recipe).data,
                        status=status.HTTP_201_CREATED)

    @action(methods=('get',), detail=False)
    def download_shopping_cart(self, request):
        user = self.request.user
        if not user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        shopping_list = '\n'.join(
            (
                f'{ingredient["name"]}: '
                f'{ingredient["amount"]} '
                f'{ingredient["measurement"]}'
                for ingredient in Ingredient.objects.filter(
                    recipe__recipe__in_carts__user=user
                ).values('name', measurement=F('measurement_unit'))
                .annotate(amount=Sum('recipe__amount'))
            )
        )
        response = HttpResponse(shopping_list,
                                content_type='text.txt; charset=utf-8')
        response['Content-Disposition'] = (
            f'attachment; filename={user.username}_shopping_list.txt')
        return response
