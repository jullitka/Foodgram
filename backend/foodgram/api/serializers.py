import base64
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import (ModelSerializer, IntegerField, ImageField,
                                        SerializerMethodField, PrimaryKeyRelatedField)

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe

from users.models import User, Subscription

class Base64ImageField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')  
            ext = format.split('/')[-1]  
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)

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

class IngredientAmountSerializer(ModelSerializer):
    id = IntegerField()
    amount = IntegerField(write_only=True)
    class Meta:
        fields = (
            'id',
            'amount',
        )
        model = IngredientRecipe


class RecipeCreateSerializer(ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = IngredientAmountSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorited',
            # 'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        model = Recipe
    
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.save()
        recipe.tags.set(tags)
        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])
            IngredientRecipe.objects.create(
                ingredient=ingredient,
                recipe=recipe,
                amount=amount
            )
        return recipe 
    
    def to_representation(self, instance):
        self.fields.pop('ingredients')
        self.fields['tags'] = TagSerializer(many=True)

        representation = super().to_representation(instance)

        representation['ingredients'] = IngredientAmountSerializer(
            IngredientRecipe.objects.filter(
                recipe=instance).all(), many=True).data
        return representation
    

class RecipeSerializer(ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientAmountSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            # 'is_favorited',
            # 'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        model = Recipe


class FavoriteSerializer(ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        model = Recipe
