from recipes.models import Favorite, ShoppingCart


def is_something(self, obj, model):
    request = self.context.get('request')
    if request.user.is_anonymous:
        return False
    if model == 'favorite':
        return Favorite.objects.filter(recipe=obj, user=request.user).exists()
    elif model == 'shopping_cart':
        return ShoppingCart.objects.filter(
            recipe=obj,
            user=request.user
        ).exists()
