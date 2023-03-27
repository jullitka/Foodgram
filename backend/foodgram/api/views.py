from django.contrib.auth import get_user_model
from django.http import HttpResponse
from djoser.views import UserViewSet

from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (AllowAny, IsAdminUser,
                                        IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import (IngredientSerializer, RecipeSerializer,
                             SubscribeSerializer, TagSerializer, CustomUserSerializer)
from recipes.models import Ingredient, Recipe, Tag

from users.models import Subscription, User


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)
    
    
    #@action(["get"], detail=False)
    #def me(self, request, *args, **kwargs):
    #    self.get_object = self.get_instance
    #    if request.user.is_anonymous:
    ##        return Response(
    #           status=status.HTTP_401_UNAUTHORIZED
    #        )
    #    else:
    #        return self.retrieve(request, *args, **kwargs)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            if user.id == author.id:
                return Response(
                    'Нельзя подписаться на себя',
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif Subscription.objects.filter(user=user, author=author).exists():
                return Response(
                    'Вы уже подписаны на данного автора',
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                subscription = Subscription.objects.create(
                    user=user, author=author
                )
                subscription.save()
                serializer = SubscribeSerializer(IsAuthenticated,
                                                 context={"request": request})
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            subscription = get_object_or_404(Subscription,
                                             user=user,
                                             author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscribers__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(pages,
                                         many=True,
                                         context={'request': request})
        return self.get_paginated_response(serializer.data)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)



class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AllowAny,)


    