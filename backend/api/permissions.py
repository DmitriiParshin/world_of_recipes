from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Для аутентифицированных пользователей имеющих статус суперпользователя
    или автора, иначе только просмотр."""

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or (
            (request.user and request.user.is_authenticated)
            and (request.user.is_superuser or obj.author == request.user)
        )
