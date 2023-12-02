import base64

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db.models import F
from rest_framework import serializers

from api.validators import ingredients_validator, tags_exist_validator
from recipes.models import Ingredient, Recipe, Tag, AmountIngredient

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        if user.is_anonymous or user == author:
            return False
        return author.subscribing.filter(user=user).exists()

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    username=validated_data['username'],
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('__all__',)


class SubscriptionSerializer(UserSerializer):
    recipes = ShortRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('password',)
        read_only_fields = ('__all__',)

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, user):
        return user.recipes.count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('__all__',)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ('__all__',)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            image_format, image = data.split(';base64,')
            ext = image_format.split('/')[-1]
            data = ContentFile(base64.b64decode(image), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'name',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, recipe):
        return recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipe__amount'),
        )

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return recipe.in_favorite.filter(user=user).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=recipe).exists()

    def validate(self, data):
        tags_ids = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')
        if not tags_ids or not ingredients:
            raise ValidationError('Недостаточно данных')
        tags = tags_exist_validator(tags_ids, Tag)
        ingredients = ingredients_validator(ingredients, Ingredient)

        data.update({'tags': tags,
                     'ingredients': ingredients,
                     'author': self.context.get('request').user})
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        AmountIngredient.objects.bulk_create(
            AmountIngredient(recipe=recipe,
                             ingredients=ingredient,
                             amount=amount)
            for ingredient, amount in ingredients.values()
        )
        return recipe

    def update(self, recipe, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        for key, value in validated_data.items():
            if hasattr(recipe, key):
                setattr(recipe, key, value)
        if tags:
            recipe.tags.clear()
            recipe.tags.set(tags)
        if ingredients:
            recipe.ingredients.clear()
            AmountIngredient.objects.bulk_create(
                AmountIngredient(recipe.pk, ingredient, amount)
                for ingredient, amount in ingredients.values())

        recipe.save()
        return recipe
