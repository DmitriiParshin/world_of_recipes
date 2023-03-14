from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import CustomUser


class RecipeTagIngredient(models.Model):
    name = models.CharField("Название", max_length=settings.LIMIT_NAME)

    class Meta:
        abstract = True
        ordering = ("name",)

    def __str__(self):
        return self.name[: settings.OUTPUT_LENGTH]


class Recipe(RecipeTagIngredient):
    author = models.ForeignKey(
        CustomUser,
        verbose_name="Автор",
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    image = models.ImageField(
        verbose_name="Изображение", upload_to="%Y/%m/%d/"
    )
    text = models.TextField(verbose_name="Описание")
    ingredients = models.ManyToManyField(
        "Ingredient",
        verbose_name="Ингредиенты",
        through="IngredientAmount",
    )
    tags = models.ManyToManyField("Tag", verbose_name="Тэги")
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления (мин)",
        validators=(
            MinValueValidator(
                settings.MIN_VALUE,
                message="Время приготовления должно быть больше 0",
            ),
        ),
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class Tag(RecipeTagIngredient):
    color = models.CharField(
        "Цветовой HEX-код",
        max_length=settings.LIMIT_COLOR,
        unique=True,
        validators=(RegexValidator(regex=r"^#([A-Fa-f0-9]{6})$"),),
    )
    slug = models.SlugField(
        "Слаг", max_length=settings.LIMIT_NAME, unique=True
    )

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"


class Ingredient(RecipeTagIngredient):
    measurement_unit = models.CharField(
        "Единицы измерения", max_length=settings.LIMIT_NAME
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "measurement_unit"], name="ingredient_unique"
            )
        ]


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="amounts",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
        related_name="amounts",
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        validators=(
            MinValueValidator(
                settings.MIN_VALUE, message="Количество должно быть больше 0"
            ),
        ),
    )

    class Meta:
        verbose_name = "Количество ингредиента"
        verbose_name_plural = "Количество ингредиентов"
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "ingredient",
                    "recipe",
                ),
                name="ingredient_amount_unique",
            ),
        )


class FavoriteShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )

    class Meta:
        abstract = True


class Favorite(FavoriteShoppingCart):
    class Meta(FavoriteShoppingCart.Meta):
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        default_related_name = "favorites"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="favorite_unique"
            )
        ]


class ShoppingCart(FavoriteShoppingCart):
    class Meta(FavoriteShoppingCart.Meta):
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        default_related_name = "carts"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="shopping_cart_unique"
            )
        ]
