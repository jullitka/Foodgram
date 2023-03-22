from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import IngredientViewSet, TagViewSet, UserViewSet

router = SimpleRouter()

router.register('users', UserViewSet)
router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]