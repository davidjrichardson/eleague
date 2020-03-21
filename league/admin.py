from django.contrib import admin

from .models import League, Division


class LeagueAdmin(admin.ModelAdmin):
    pass


class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_count')
    search_fields = ('name',)
    ordering = ('name',)

    def team_count(self, value: Division) -> str:
        if value.max_teams == -1:
            return 'Unlimited'
        else:
            return str(value.max_teams)

    team_count.admin_order_field = 'max_teams'


admin.site.register(League, LeagueAdmin)
admin.site.register(Division, DivisionAdmin)
