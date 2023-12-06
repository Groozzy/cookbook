from django.core.exceptions import ValidationError


def ingredients_validator(ingredients, ingredient_model):
    if not ingredients:
        raise ValidationError('Ингредиенты отсутствуют')

    validated_ingredients = {}

    for ingredient in ingredients:
        if not (isinstance(ingredient['amount'], int)
                or ingredient['amount'].isdigit()):
            raise ValidationError('Некорректный формат ингредиента')

        validated_ingredients[ingredient['id']] = int(ingredient['amount'])
        if validated_ingredients[ingredient['id']] <= 0:
            raise ValidationError('Количество должно быть больше нуля')
        elif validated_ingredients[ingredient['id']] >= 10000:
            raise ValidationError('У меня столько посуды нет!')

    if not validated_ingredients:
        raise ValidationError('Корректные ингредиенты отсутствуют')

    available_ingredients = ingredient_model.objects.filter(
        pk__in=validated_ingredients.keys())

    if not available_ingredients:
        raise ValidationError('В базе не указаны доступные ингредиенты')

    for ingredient in available_ingredients:
        validated_ingredients[ingredient.pk] = (
            ingredient,
            validated_ingredients[ingredient.pk]
        )

    return validated_ingredients


def tags_exist_validator(tags_ids, tag):
    if not tags_ids:
        raise ValidationError('Теги отсутствуют')

    tags = tag.objects.filter(id__in=tags_ids)

    if len(tags) != len(tags_ids):
        raise ValidationError('Указан несуществующий тег')

    return tags
