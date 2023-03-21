from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import IngredientViewSet, TagViewSet

router = SimpleRouter()

router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls))
]