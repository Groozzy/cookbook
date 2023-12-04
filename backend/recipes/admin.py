from django.contrib import admin

from recipes import models, forms


class IngredientInline(admin.TabularInline):
    model = models.AmountIngredient
    extra = 1


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'author', 'added_in_favorites')
    readonly_fields = ('added_in_favorites',)
    list_filter = ('author', 'name')
    exclude = ('ingredients',)
    fieldsets = ((None, {'fields': (
        'name', 'author', 'tags', 'image', 'cooking_time', 'text')}),)
    filter_horizontal = ('tags',)
    inlines = (IngredientInline,)

    @admin.display(description='Количество добавлений в избранное')
    def added_in_favorites(self, recipe):
        return recipe.in_favorite.count()


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    fieldsets = ((None, {'fields': ('name', 'slug', 'color')}),)


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    form = forms.TagForm
    list_display = ('name', 'slug', 'color')


@admin.register(models.ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(models.Favorite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(models.AmountIngredient)
class AmountIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
