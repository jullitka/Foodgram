from django.contrib import admin

from .models import (Ingredient, IngredientRecipe,
                     Recipe, Tag, TagRecipe)

admin.site.register(Tag)
admin.site.register(TagRecipe)
admin.site.register(IngredientRecipe)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('author',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)

