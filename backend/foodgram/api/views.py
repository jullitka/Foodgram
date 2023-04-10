from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import IngredientFilter,  RecipeFilter
from api.paginations import CustomPagination
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.serializers import (CustomUserSerializer, IngredientSerializer,
                             RecipeCreateSerializer, RecipeSerializer,
                             RecipeShortSerializer, SubscribeSerializer,
                             TagSerializer)
from recipes.models import (Favorite, Ingredient,
                            IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from users.models import Subscription, User


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPagination

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        """Подписаться и отписаться от пользователя с известным id"""
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            if user.id == author.id:
                return Response(
                    {'errors': 'Нельзя подписаться на себя'},
                    status=HTTP_400_BAD_REQUEST
                )
            elif Subscription.objects.filter(
                user=user, author=author
            ).exists():
                return Response(
                    {'errors': 'Вы уже подписаны на данного автора'},
                    status=HTTP_400_BAD_REQUEST
                )
            else:
                subscription = Subscription.objects.create(
                    user=user, author=author
                )
                serializer = SubscribeSerializer(author,
                                                 context={"request": request})
                return Response(serializer.data, status=HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = Subscription.objects.filter(
                user=user, author=author
            )
            if subscription.exists():
                subscription.delete()
                return Response(status=HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'errors': 'Вы не были подписаны на этого автора'},
                    status=HTTP_400_BAD_REQUEST)

    @action(detail=False,
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        """Список подписок текущего авторизованного пользователя"""
        user = request.user
        queryset = User.objects.filter(subscribers__user=user)
        serializer = SubscribeSerializer(
            self.paginate_queryset(queryset),
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('^name',)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        """Добавить рецепт в избранное или удалить"""
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'errors': 'Вы уже добавили этот рецепт в избранное'},
                    status=HTTP_400_BAD_REQUEST
                )
            else:
                favorite = Favorite.objects.create(
                    user=user, recipe=recipe
                )
                serializer = RecipeShortSerializer(
                    recipe, context={"request": request}
                )
                return Response(serializer.data, status=HTTP_201_CREATED)

        elif request.method == 'DELETE':
            favorite = Favorite.objects.filter(user=user, recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response(status=HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'errors': 'Вы не добавляли этот рецепт в избранное'},
                    status=HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        """Добавить рецепт в список покупок или удалить """
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'errors': 'Вы уже добавили этот рецепт в список покупок'},
                    status=HTTP_400_BAD_REQUEST
                )
            else:
                favorite = ShoppingCart.objects.create(
                    user=user, recipe=recipe
                )
                serializer = RecipeShortSerializer(
                    recipe, context={"request": request}
                )
                return Response(serializer.data, status=HTTP_201_CREATED)

        elif request.method == 'DELETE':
            favorite = ShoppingCart.objects.filter(user=user, recipe=recipe)
            if favorite.exists():
                favorite.delete()
                return Response(status=HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'errors': 'Вы не добавляли этот рецепт в список покупок'},
                    status=HTTP_400_BAD_REQUEST)

    @action(detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Получение списка продуктов из рецептов"""
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(user=user).values('recipe')
        recipes = [recipe['recipe'] for recipe in shopping_cart]
        buy_list = IngredientRecipe.objects.filter(recipe__in=recipes).values(
            'ingredient__name', 'ingredient__measurement_unit'
            ).annotate(total_amount=Sum('amount'))
        ingredients = []
        for ingredient in buy_list:
            ingredient_text = (
                f"- {ingredient['ingredient__name']} "
                f"({ingredient['ingredient__measurement_unit']})"
                f" - {ingredient['total_amount']}"
            )
            ingredients.append(ingredient_text)
            filename = f'shopping_cart_for_{user.username}'
            '\n'.join(ingredients)
        response = HttpResponse('Cписок покупок:\n' + '\n'.join(ingredients),
                                content_type='text/plain')
        response['Content-Disposition'] = (f'attachment; filename={filename}')
        return response

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.image.delete()
        instance.delete()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeSerializer
        return RecipeCreateSerializer
