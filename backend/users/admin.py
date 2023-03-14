from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import CustomUser, Follow

admin.site.unregister(Group)


class FollowInline(admin.TabularInline):
    model = Follow
    extra = 1
    fk_name = "user"


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    inlines = (FollowInline,)
    list_display = (
        "id",
        "username",
        "email",
        "amount_recipes",
        "amount_following",
        "amount_followers",
    )
    list_display_links = ("username",)
    search_fields = ("username", "email")
    list_filter = ("username", "email")

    def amount_recipes(self, obj):
        return obj.recipes.count()

    amount_recipes.short_description = "Кол-во рецептов"

    def amount_following(self, obj):
        return obj.following.count()

    amount_following.short_description = "Кол-во подписчиков"

    def amount_followers(self, obj):
        return obj.follower.count()

    amount_followers.short_description = "Кол-во подписок"
