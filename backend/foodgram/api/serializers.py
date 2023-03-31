import base64
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import (ModelSerializer, IntegerField, ImageField,
                                        SerializerMethodField, PrimaryKeyRelatedField)

from recipes.models import (Favorite, Ingredient, IngredientRecipe,
                            Recipe, ShoppingCart, Tag, TagRecipe)

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
    recipes_count = SerializerMethodField()
    recipes = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed',
            'recipes'
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Subscription.objects.filter(author=obj, user=request.user).exists()
    
    def recipes_count(self, obj):
        return obj.recipes.count()
    
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


class IngredientRecipeSerializer(ModelSerializer):
    id = SerializerMethodField()
    name = SerializerMethodField()
    measurement_unit = SerializerMethodField()
    
    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )
        model = IngredientRecipe
    
    def get_id(self, obj):
        return obj.ingredient.id
    
    def get_name(self, obj):
        return obj.ingredient.name
    
    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class RecipeCreateSerializer(ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = IngredientAmountSerializer(many=True)
    image = Base64ImageField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        model = Recipe
    
    def ingredients_to_recipe(self, ingredients, recipe):
        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])
            IngredientRecipe.objects.create(
                ingredient=ingredient,
                recipe=recipe,
                amount=amount
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.ingredients_to_recipe(self, ingredients, recipe)
        return recipe 
    
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.ingredients_to_recipe(ingredients, instance)
        instance.save()
        return instance 


    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance,
                                    context=context).data
       
    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj, user=request.user).exists()
    
    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipe=obj, user=request.user).exists()


class RecipeSerializer(ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = SerializerMethodField()
    image = Base64ImageField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        model = Recipe

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj, user=request.user).exists()
    
    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipe=obj, user=request.user).exists()

    def get_ingredients(self, obj):
        ingredients = IngredientRecipe.objects.filter(recipe=obj)
        serializer = IngredientRecipeSerializer(ingredients, many=True)
        return serializer.data


class FavoriteSerializer(ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        model = Recipe

