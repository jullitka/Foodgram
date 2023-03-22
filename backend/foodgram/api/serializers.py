from django.contrib.auth import get_user_model
from rest_framework.serializers import (EmailField, ModelSerializer,
                                        RegexField, ValidationError)

from recipes.models import Ingredient, Tag

User = get_user_model()

class UserSerializer(ModelSerializer):
    email = EmailField(max_length=254,
                       required=True)
    username = RegexField(max_length=150,
                          regex=r'^[\w.@+-]+\z')

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )

class IngredientSerializer(ModelSerializer):
    class Meta:
        fields = fields = '__all__'
        model = Ingredient

class TagSerializer(ModelSerializer):
    class Meta:
        fields = fields = '__all__'
        model = Tag


