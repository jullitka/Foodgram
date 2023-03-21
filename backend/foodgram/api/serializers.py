from http import HTTPStatus
from rest_framework.serializers import ModelSerializer, ValidationError

from recipes.models import Ingredient, Tag

class IngredientSerializer(ModelSerializer):
    class Meta:
        fields = fields = '__all__'
        model = Ingredient

class TagSerializer(ModelSerializer):
    class Meta:
        fields = fields = '__all__'
        model = Tag


