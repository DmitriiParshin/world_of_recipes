from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CustomUserViewSet, FollowListView, FollowViewSet

router = DefaultRouter()
router.register("users", CustomUserViewSet, basename="users")

urlpatterns = [
    path(
        "users/subscriptions/",
        FollowListView.as_view(),
        name="subscriptions",
    ),
    path(
        "users/<int:pk>/subscribe/",
        FollowViewSet.as_view(),
        name="subscribe",
    ),
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]