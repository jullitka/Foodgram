from django.contrib.auth import get_user_model
from django.http import HttpResponse
from djoser.views import UserViewSet

from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAdminUser,
                                        IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import (IngredientSerializer, RecipeSerializer, RecipeCreateSerializer,
                             SubscribeSerializer, TagSerializer, CustomUserSerializer)
from recipes.models import Ingredient, Recipe, Tag

from users.models import Subscription, User


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        """Подписаться и отписаться от пользователя с известным id"""
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            if user.id == author.id:
                return Response(
                    {'errors':'Нельзя подписаться на себя'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif Subscription.objects.filter(user=user, author=author).exists():
                return Response(
                    {'errors':'Вы уже подписаны на данного автора'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                subscription = Subscription.objects.create(
                    user=user, author=author
                )
                serializer = SubscribeSerializer(author,
                                                 context={"request": request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = Subscription.objects.filter(user=user, author=author)
            if subscription.exists():
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'errors': 'Вы не были подписаны на этого автора'},
                    status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
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
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)



class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    # serializer_class = RecipeSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action =='list' or self.action == 'retrieve':
            return RecipeSerializer
        return RecipeCreateSerializer
    