# Generated by Django 3.2.16 on 2023-12-06 00:21

import django.core.validators
from django.db import migrations, models
import recipes.enums


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_alter_recipe_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amountingredient',
            name='amount',
            field=models.PositiveSmallIntegerField(default=recipes.enums.AmountIngredientEnums['AMOUNT_DEFAULT_VALUE'], validators=[django.core.validators.MinValueValidator(recipes.enums.AmountIngredientEnums['AMOUNT_DEFAULT_VALUE'], 'Укажите количество!'), django.core.validators.MaxValueValidator(recipes.enums.AmountIngredientEnums['AMOUNT_MAX_VALUE'], 'У меня столько посуды нет!')], verbose_name='Количество'),
        ),
    ]
