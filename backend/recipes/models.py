from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from recipes import enums

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Тег',
        max_length=enums.TagEnums.NAME_MAX_LEN,
        unique=True,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=enums.TagEnums.SLUG_MAX_LEN,
        unique=True,
        db_index=False,
    )
    color = ColorField(
        'Цвет',
        format='hex',
        max_length=enums.TagEnums.COLOR_MAX_LEN,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('slug',)

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    name = models.CharField(
        'Ингредиент',
        max_length=enums.IngredientEnums.NAME_MAX_LEN
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=enums.IngredientEnums.MEASUREMENT_UNIT_MAX_LEN
    )

    class Meta:
        verbose_name = 'Ингредиент',
        verbose_name_plural = 'Ингредиенты'
        ordering = ('id',)
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='Ингредиент уже существует!',
            ),
        )

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Recipe(models.Model):
    name = models.CharField(
        'Название',
        max_length=enums.RecipeEnums.NAME_MAX_LEN,
        validators=(
            validators.MinLengthValidator(
                enums.RecipeEnums.NAME_MIN_LEN,
                'Название слишком короткое'
            ),
        )
    )
    author = models.ForeignKey(
        User,
        models.SET_NULL,
        related_name='recipes',
        verbose_name='Автор',
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингредиенты',
    )
    image = models.ImageField('Изображение', upload_to='images/')
    text = models.TextField(
        'Описание',
        max_length=enums.RecipeEnums.TEXT_MAX_LEN
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        default=enums.RecipeEnums.COOKING_TIME_DEFAULT_VALUE,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='recipe_duplication_constraint',
            ),
        )

    def __str__(self):
        return f'"{self.name}". Автор: {self.author}'


class AmountIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        models.CASCADE,
        related_name='ingredient',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        models.CASCADE,
        related_name='recipe',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        default=enums.AmountIngredientEnums.AMOUNT_DEFAULT_VALUE,
        validators=(
            validators.MinValueValidator(
                enums.AmountIngredientEnums.AMOUNT_MIN_VALUE,
                'Укажите количество!'
            ),
        )
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ('recipe', 'ingredient')
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_ingredient_amount_constraint',
            ),
        )

    def __str__(self):
        return (f'{self.recipe.name} {self.ingredient.name}'
                f' {self.amount} {self.ingredient.measurement_unit}')


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        models.CASCADE,
        related_name='in_favorite',
        verbose_name='Рецепт',
    )
    user = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='favorite_recipies',
        verbose_name='Пользователь',
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ('user',)
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_favorites_constraint',
            ),
        )

    def __str__(self):
        return f'{self.recipe} <- {self.user}'


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        models.CASCADE,
        related_name='in_carts',
        verbose_name='Рецепт',
    )
    user = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'
        ordering = ('user',)
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_recipe_in_cart_constraint',
            ),
        )

    def __str__(self):
        return f'{self.recipe} <- {self.user}'
