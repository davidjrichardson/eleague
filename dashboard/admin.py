from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import ELeagueUser


class ELeagueUserInline(admin.StackedInline):
    model = ELeagueUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'university', 'is_staff')
    search_fields = ('username', 'email', 'eleagueuser__university',)

    inlines = (ELeagueUserInline,)

    def university(self, obj: User) -> str:
        return ELeagueUser.objects.get(user=obj).university

    university.admin_order_field = 'eleagueuser__university'
    ordering = ('eleagueuser__university',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
