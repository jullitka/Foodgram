from django_filters.rest_framework import CharFilter, FilterSet
from django_filters.rest_framework.filters import (BooleanFilter,
                                                   ModelMultipleChoiceFilter)

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
                                     field_name='tags__slug',
                                     to_field_name='slug')
    is_favorited = BooleanFilter(method='is_favorited_filter')
    is_in_shopping_cart = BooleanFilter(method='is_in_shopping_cart_filter')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart',)

    def is_favorited_filter(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping_cart__user=user)
        return queryset
