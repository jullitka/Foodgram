from django.core.validators import RegexValidator
from django.db.models import (CASCADE, CharField, DateTimeField, IntegerField,
                              ImageField, ForeignKey, ManyToManyField, Model,
                              SlugField, TextField, UniqueConstraint)

from users.models import User


class Tag(Model):
    name = CharField(
        max_length=50,
        unique=True,
        verbose_name='Тег'
    )
    color = CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет',
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Необходимо ввести цвет в формате HEX'
            )
        ])
    slug = SlugField(unique=True, verbose_name='Адрес')

    def __str__(self):
        return self.name


class Ingredient(Model):
    name = CharField(
        max_length=50,
        verbose_name='Название ингредиента'
    )
    measurement_unit = CharField(
        max_length=10,
        verbose_name='Единица измерения'
        )
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=('name', 'measurement_unit'), name='ingredient')
        ]

    def __str__(self):
        return self.name


class Recipe(Model):
    ingredients = ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
        help_text='Выберите ингредиенты',
        related_name='recipes'
    )
    tags = ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Теги',
        help_text='Выберите теги',
        related_name='recipes'
    )
    image = ImageField(
        verbose_name= 'Картинка',
        upload_to='recipes/'
    )
    name = CharField(
        max_length=100,
        verbose_name='Название блюда',
        help_text='Введите название блюда'
    )
    text = TextField(
        verbose_name='Текст рецепта',
        help_text='Введите текст рецепта'
    )
    cooking_time = IntegerField(
        verbose_name='Время приготовления',
        help_text='Введите имя приготовления в минутах')
    author = ForeignKey(
        User,
        related_name='recipes',
        verbose_name='Автор',
        on_delete=CASCADE
    )
    pub_date = DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(Model):
    ingredient = ForeignKey(
        Ingredient,
        on_delete=CASCADE,
        related_name='ingredient'
    )
    recipe = ForeignKey(Recipe, on_delete=CASCADE)
    amount = IntegerField(verbose_name='Количество')


class TagRecipe(Model):
    tag = ForeignKey(Tag, on_delete=CASCADE)
    recipe = ForeignKey(Recipe, on_delete=CASCADE)


class Favorite(Model):
    user = ForeignKey(
        User,
        related_name='favorites',
        verbose_name='Пользователь',
        on_delete=CASCADE
    )
    recipe = ForeignKey(
        Recipe,
        related_name='favorites',
        verbose_name='Рецепт',
        on_delete=CASCADE
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=('recipe', 'user'), name='favorite')
        ]

    def __str__(self):
        return f'{self.recipe} в избранном {self.user}'
    
class ShoppingCart(Model):
    user = ForeignKey(
        User,
        related_name='shopping_cart',
        verbose_name='Пользователь',
        on_delete=CASCADE
    )
    recipe = ForeignKey(
        Recipe,
        related_name='shopping_cart',
        verbose_name='Рецепт',
        on_delete=CASCADE
    )
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=('recipe', 'user'), name='shopping_cart')
        ]

    def __str__(self):
        return f'"{self.recipe}" в списке покупок {self.user}'