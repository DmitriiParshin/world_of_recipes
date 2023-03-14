from django.contrib.admin import ModelAdmin, TabularInline, register

from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ("id", "name", "slug")


class IngredientAmountInline(TabularInline):
    model = IngredientAmount
    min_num = 1


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    inlines = [
        IngredientAmountInline,
    ]
    list_display = (
        "id",
        "name",
        "author",
        "amount_favorites",
        "get_tags",
        "get_ingredients",
    )
    list_display_links = ("name",)
    list_filter = ("author", "name", "tags")
    search_fields = ("name",)

    def amount_favorites(self, obj):
        return obj.favorites.count()

    amount_favorites.short_description = "В избранном"

    def get_tags(self, obj):
        return ", ".join([str(_) for _ in obj.tags.all()])

    get_tags.short_description = "Тэги"

    def get_ingredients(self, obj):
        return ", ".join([str(_) for _ in obj.ingredients.all()])

    get_ingredients.short_description = "Ингредиенты"


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ("id", "name", "measurement_unit")


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ("id", "user", "recipe")


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ("id", "user", "recipe")
