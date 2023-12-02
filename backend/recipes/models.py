from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy


User = get_user_model()


class Tag(models.Model):
    class Color(models.TextChoices):
        GREEN = 'green', gettext_lazy('#00FF00')
        RED = 'red', gettext_lazy('#FF0000')
        BLUE = 'blue', gettext_lazy('#0000FF')
        PURPLE = 'purple', gettext_lazy('#800080')

    name = models.CharField(
        'Тег',
        max_length=32,
        unique=True,
    )
    slug = models.SlugField(
        'Слаг',
        max_length=32,
        unique=True,
        db_index=False,
    )
    color = models.CharField(
        'Цвет',
        max_length=7,
        unique=True,
        db_index=False,
        choices=Color.choices,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    name = models.CharField('Ингредиент', max_length=64)
    measurement_unit = models.CharField('Единица измерения', max_length=32)

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
        max_length=64,
        validators=(
            validators.MinLengthValidator(3, 'Название слишком короткое'),
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
    text = models.TextField('Описание', max_length=1024)
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        default=5,
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
    ingredients = models.ForeignKey(
        Ingredient,
        models.CASCADE,
        related_name='recipe',
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        default=1,
        validators=(validators.MinValueValidator(1, 'Укажите количество!'),)
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ('recipe', 'ingredients')
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredients'),
                name='unique_ingredient_amount_constraint',
            ),
        )

    def __str__(self):
        return (f'{self.recipe.name} {self.ingredients.name}'
                f' {self.amount} {self.ingredients.measurement_unit}')


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
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user'),
                name='unique_recipe_in_cart_constraint',
            ),
        )

    def __str__(self):
        return f'{self.recipe} <- {self.user}'
