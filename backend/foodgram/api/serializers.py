from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField, PrimaryKeyRelatedField)

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe

from users.models import User, Subscription

class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Subscription.objects.filter(author=obj, user=request.user).exists()
 

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name'
        )

class SubscribeSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed',
            'recipes'
           # 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Subscription.objects.filter(author=obj, user=request.user).exists()
    
    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return recipes
    
class IngredientSerializer(ModelSerializer):
    class Meta:
        fields = fields = '__all__'
        model = Ingredient


class TagSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class RecipeCreateSerializer(ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = SerializerMethodField()
    # ingredients = PrimaryKeyRelatedField(many=True, queryset=Ingredient.objects.all())

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'name',
            'ingredients',
            'cooking_time'
        )
        model = Recipe
    
    def get_ingredients(self, obj):
        request = self.context.get('request')

class RecipeSerializer(ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'name',
            'ingredients',
            'cooking_time'
        )
        model = Recipe

    #def create(self, validated_data):
    #    tags = validated_data.pop('tags')
    #    recipe = Recipe.objects.create(**validated_data)
    #    recipe.save()
    #    recipe.tags.set(tags)
    #    return recipe 