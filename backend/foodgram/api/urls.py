from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import IngredientViewSet, TagViewSet, CustomUserViewSet, RecipeViewSet

router = SimpleRouter()

router.register(r'users', CustomUserViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

