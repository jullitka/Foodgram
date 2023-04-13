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
    is_favorited = BooleanFilter(
        field_name='is_favorited',
        method='is_something'
    )
    is_in_shopping_cart = BooleanFilter(
        field_name='is_in_shopping_cart',
        method='is_something'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart',)

    def is_something(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if name == 'is_favorited' and value:
                return queryset.filter(favorites__user=user)
            if name == 'in_is_shopping_cart' and value:
                return queryset.filter(shopping_cart__user=user)
            return queryset
        return queryset