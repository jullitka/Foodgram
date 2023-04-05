from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from .models import (Favorite, Ingredient, IngredientRecipe,
                     Recipe, ShoppingCart, Tag, TagRecipe)


class IngredientRecipeInline(TabularInline):
    model = IngredientRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author', 'total_favorites' )
    list_filter = ('author', 'name', 'tags', 'pub_date')
    search_fields = ('author', 'name', 'tags')
    inlines = (IngredientRecipeInline,)
    
    @admin.display(description='В избранном')
    def total_favorites(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')
    inlines = (IngredientRecipeInline,)


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient')
    list_filter = ('recipe', 'ingredient')


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_filters = ('name')
    search_fields = ('name', 'color', 'slug')


@admin.register(TagRecipe)
class TagRecipeAdmin(ModelAdmin):
    list_display = ('recipe', 'tag')
    list_filters = ('recipe', 'tag')
    search_fields = ('recipe', 'tag')    


@admin.register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user', 'recipe')

