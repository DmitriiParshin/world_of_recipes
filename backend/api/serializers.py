from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.fields import (IntegerField, ReadOnlyField,
                                   SerializerMethodField)
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer

from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from users.models import CustomUser, Follow


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(read_only=True)
    recipes = SerializerMethodField(read_only=True)
    recipes_count = SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if not request.user.is_anonymous:
            return Follow.objects.filter(
                user=request.user, author=obj
            ).exists()

    def get_recipes(self, obj):
        request = self.context.get("request")
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get("recipes_limit")
        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
        return ShortRecipeSerializer(recipes, many=True).data

    @staticmethod
    def get_recipes_count(obj):
        return obj.recipes.count()


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        read_only_fields = ("__all__",)


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"
        read_only_fields = ("__all__",)


class IngredientAmountSerializer(ModelSerializer):
    id = ReadOnlyField(source="ingredient.id")
    name = ReadOnlyField(source="ingredient.name")
    measurement_unit = ReadOnlyField(source="ingredient.measurement_unit")

    class Meta:
        model = IngredientAmount
        fields = ("id", "name", "amount", "measurement_unit")


class RecipeListSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = SerializerMethodField(read_only=True)
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = "__all__"

    @staticmethod
    def get_ingredients(obj):
        return IngredientAmountSerializer(
            IngredientAmount.objects.filter(recipe=obj), many=True
        ).data

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if not request.user.is_anonymous:
            return Favorite.objects.filter(
                user=request.user, recipe=obj
            ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if not request.user.is_anonymous:
            return ShoppingCart.objects.filter(
                user=request.user, recipe=obj
            ).exists()


class AddIngredientSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ("id", "amount")


class RecipeSerializer(ModelSerializer):
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    ingredients = AddIngredientSerializer(many=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "author",
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def validate(self, data):
        ingredients = data["ingredients"]
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient["id"]
            if ingredient_id in ingredients_list:
                raise ValidationError(
                    {"ingredients": "Ингредиенты должны быть уникальными!"}
                )
            ingredients_list.append(ingredient_id)
            amount = ingredient["amount"]
            if not int(amount):
                raise ValidationError(
                    {"amount": "Хотя бы один ингредиент должен быть!"}
                )

        tags = data["tags"]
        if not tags:
            raise ValidationError({"tags": "Хотя бы один тэг должен быть!"})
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError(
                    {"tags": "Тэги должны быть уникальными!"}
                )
            tags_list.append(tag)

        cooking_time = data["cooking_time"]
        if not int(cooking_time):
            raise ValidationError(
                {"cooking_time": "Время приготовления должно быть больше 0!"}
            )
        return data

    @staticmethod
    def create_ingredients(ingredients, recipe):
        data_to_create = [
            IngredientAmount(
                recipe=recipe,
                ingredient=ingredient["id"],
                amount=ingredient["amount"],
            )
            for ingredient in ingredients
        ]
        IngredientAmount.objects.bulk_create(data_to_create)

    @staticmethod
    def create_tags(tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    def create(self, validated_data):
        author = self.context.get("request").user
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def to_representation(self, instance):
        request = self.context.get("request")
        context = {"request": request}
        return RecipeListSerializer(instance, context=context).data

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.create_tags(validated_data.pop("tags"), instance)
        self.create_ingredients(validated_data.pop("ingredients"), instance)
        return super().update(instance, validated_data)


class ShortRecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = ("user", "recipe")

    def validate(self, data):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        recipe = data["recipe"]
        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            raise ValidationError({"status": "Рецепт уже есть в избранном!"})
        return data

    def to_representation(self, instance):
        request = self.context.get("request")
        context = {"request": request}
        return ShortRecipeSerializer(instance.recipe, context=context).data


class ShoppingCartSerializer(ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ("user", "recipe")

    def validate(self, data):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        recipe = data["recipe"]
        if ShoppingCart.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            raise ValidationError({"status": "Рецепт уже есть в корзине!"})
        return data

    def to_representation(self, instance):
        request = self.context.get("request")
        context = {"request": request}
        return ShortRecipeSerializer(instance.recipe, context=context).data


class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"
        read_only_fields = ("__all__",)

    def validate(self, data):
        author = self.instance
        user = self.context.get("request").user
        if user == author:
            raise ValidationError(
                detail="Нельзя подписаться на себя",
                code=status.HTTP_400_BAD_REQUEST,
            )
        if Follow.objects.filter(user=user, author=author).exists():
            raise ValidationError(
                detail="Вы уже подписаны на этого пользователя!",
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data
