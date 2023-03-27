from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import (ReadOnlyField, EmailField, ModelSerializer,
                                        RegexField,  SerializerMethodField)

from recipes.models import Ingredient, Recipe, Tag

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

    #recipes = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed',
           # 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Subscription.objects.filter(author=obj, user=request.user).exists()
    #def get_recipes(self, id):
        #return Recipe.objects.filter(author = )
    
    #def get_recipes_count(self, id)


class IngredientSerializer(ModelSerializer):
    class Meta:
        fields = fields = '__all__'
        model = Ingredient


class TagSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class RecipeSerializer(ModelSerializer):
    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
        )
