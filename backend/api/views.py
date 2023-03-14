from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import IngredientSearchFilter, RecipeFilter
from api.pagination import CustomPageNumberPagination
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CustomUserSerializer, FavoriteSerializer,
                             FollowSerializer, IngredientSerializer,
                             RecipeListSerializer, RecipeSerializer,
                             ShoppingCartSerializer, TagSerializer)
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from users.models import CustomUser, Follow


class TagsViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = IngredientSerializer
    filter_backends = [IngredientSearchFilter]
    search_fields = ("^name",)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all().order_by("-pub_date")
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeListSerializer
        return RecipeSerializer

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {"user": request.user.id, "recipe": pk}
        serializer = serializers(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        get_object_or_404(
            model, user=request.user, recipe=get_object_or_404(Recipe, id=pk)
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True, methods=["post"], permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorite
        )

    @action(
        detail=True, methods=["post"], permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=ShoppingCartSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCart
        )

    @action(
        detail=False, methods=["get"], permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = (
            IngredientAmount.objects.filter(recipe__carts__user=request.user)
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(amount__sum=Sum("amount"))
            .order_by("ingredient__name")
        )
        return self.construct_pdf(ingredients)

    @staticmethod
    def construct_pdf(data):
        pdfmetrics.registerFont(
            TTFont("Comic Sans MS", "data/Comic Sans MS.ttf", "UTF-8")
        )
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            "attachment; " 'filename="recipe.pdf"'
        )
        page = canvas.Canvas(response)
        page.setFont("Comic Sans MS", size=24)
        page.drawString(200, 800, "список покупок")
        page.setFont("Comic Sans MS", size=16)
        page.drawString(75, 750, "Ингредиенты:")
        height = 700
        for i, ingredient_data in enumerate(data, 1):
            page.drawString(
                75,
                height,
                (
                    f'{i}. {ingredient_data["ingredient__name"]} - '
                    f'{ingredient_data["amount__sum"]} '
                    f'{ingredient_data["ingredient__measurement_unit"]}'
                ),
            )
            height -= 25
        page.showPage()
        page.save()
        return response


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination


class FollowViewSet(APIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    @staticmethod
    def post(request, pk):
        data = {
            "user": request.user.id,
            "author": pk,
        }
        serializer = FollowSerializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete(request, pk):
        get_object_or_404(
            Follow,
            user=request.user.id,
            author=get_object_or_404(CustomUser, id=pk),
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListView(ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get(self, request, *args, **kwargs):
        following = CustomUser.objects.filter(
            following__user=self.request.user
        )
        print(following)
        pages = self.paginate_queryset(following)
        serializer = CustomUserSerializer(
            pages, many=True, context={"request": self.request}
        )
        return self.get_paginated_response(serializer.data)
