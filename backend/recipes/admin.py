from django.contrib import admin

from recipes import models

admin.site.register(models.AmountIngredient)
admin.site.register(models.Favorite)
admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)
admin.site.register(models.ShoppingCart)
admin.site.register(models.Tag)
