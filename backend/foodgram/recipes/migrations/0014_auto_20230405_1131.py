# Generated by Django 3.2.18 on 2023-04-05 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_auto_20230405_1128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredientrecipe',
            options={'verbose_name': 'Ингредиент для рецепта', 'verbose_name_plural': 'Ингредиенты для рецепта'},
        ),
        migrations.AlterModelOptions(
            name='tagrecipe',
            options={'verbose_name': 'Тег рецепта', 'verbose_name_plural': 'Теги рецептов'},
        ),
    ]
