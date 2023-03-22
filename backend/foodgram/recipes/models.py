from django.contrib.auth import get_user_model
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Тег'
    )
    color = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Цвет')
    slug = models.SlugField(unique=True, verbose_name='Адрес')

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=10,
        verbose_name='Единица измерения'
        )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
        help_text='Выберите ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Теги',
        help_text='Выберите теги')
    # image = models.ImageField()
    name = models.CharField(
        max_length=100,
        verbose_name='Название блюда',
        help_text='Введите название блюда'
    )
    text = models.TextField(
        verbose_name='Текст рецепта',
        help_text='Введите текст рецепта'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='Введите имя приготовления в минутах')
    author = models.ForeignKey(
        User,
        related_name='recipes',
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
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


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество')


class TagRecipe(models.Model):
    ingredient = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)