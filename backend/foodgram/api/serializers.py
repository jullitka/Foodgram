from django.contrib.auth import get_user_model
from rest_framework.serializers import (BooleanField, EmailField, ModelSerializer,
                                        RegexField,  SerializerMethodField)

from recipes.models import Ingredient, Recipe, Tag

from users.models import User, Subscription

class UserSerializer(ModelSerializer):
    email = EmailField(max_length=254,
                       required=True)
    username = RegexField(max_length=150,
                          regex=r'^[\w.@+-]+\z')
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


class SubscribeSerializer(ModelSerializer):
    is_subscribed = BooleanField(read_only=True)
    #recipes = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed',
           # 'recipes', 'recipes_count'
        )

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
