from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import Ingredient, IngredientAmount, Recipe, Tag
from users.models import Follow
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientAmount.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        source='ingredientamount_set',
        many=True,
        read_only=True,
    )
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')

        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Нужен хоть один ингредиент для рецепта.'
            })

        ingredient_counts = {}
        for ingredient_item in ingredients:
            ingredient_id = ingredient_item['id']
            if ingredient_id in ingredient_counts:
                ingredient_counts[ingredient_id] += 1
            else:
                ingredient_counts[ingredient_id] = 1

            if int(ingredient_item['amount']) <= 0:
                raise serializers.ValidationError({
                    'ingredients': 'Кол-во ингредиентов должно быть больше 0.'
                })

        duplicates = [
            ingredient_id for ingredient_id,
            count in ingredient_counts.items() if count > 1
        ]

        if duplicates:
            duplicate_names = [
                Ingredient.objects.get(id=id).name for id in duplicates
            ]
            raise serializers.ValidationError({
                'ingredients': f'Ингредиенты должны быть уникальными. '
                               f'Повторяются: {", ".join(duplicate_names)}.'
            })

        data['ingredients'] = ingredients
        return data

    def create_ingredients(self, ingredients, recipe):
        ingredient_amount_objects = [
            IngredientAmount(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
            for ingredient in ingredients
        ]
        IngredientAmount.objects.bulk_create(ingredient_amount_objects)

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        if tags_data:
            if len(tags_data) != len(set(tags_data)):
                raise serializers.ValidationError(
                    'Повторяющиеся теги не допускаются.'
                )
            recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientAmount.objects.filter(recipe=instance).all().delete()
        self.create_ingredients(validated_data.get('ingredients'), instance)
        instance.save()
        return instance


class CropRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return CropRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
