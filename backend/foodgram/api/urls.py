from django.urls import include, path
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register('recipes', RecipeViewSet)