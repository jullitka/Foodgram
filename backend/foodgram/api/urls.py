from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (IngredientViewSet, TagViewSet,
                       CustomUserViewSet, RecipeViewSet)

router = SimpleRouter()

router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
