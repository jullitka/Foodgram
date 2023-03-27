from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import IngredientViewSet, TagViewSet, CustomUserViewSet

router = SimpleRouter()

router.register(r'users', CustomUserViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'tags', TagViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path(
        'users/<int:pk>/subscribe/',
        CustomUserViewSet.as_view({'get': 'subscribe',}),
        name='subscribe'
    ),
    path('auth/', include('djoser.urls.authtoken')),
]

