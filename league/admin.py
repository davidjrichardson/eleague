from django.contrib import admin

from .models import League, Division, LeagueSplit, Round, Archer


class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'round', 'start_at', 'end_at')
    search_fields = ('name', 'description')
    list_filter = ('round__type', 'round__season')
    ordering = ('end_at',)


class LeagueSplitAdmin(admin.ModelAdmin):
    list_display = ('name', 'split_ends')
    search_fields = ('name',)


class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_count')
    search_fields = ('name',)

    def team_count(self, value: Division) -> str:
        if value.max_teams == -1:
            return 'Unlimited'
        else:
            return str(value.max_teams)

    team_count.admin_order_field = 'max_teams'


class RoundAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'season')
    search_fields = ('name', 'description')
    list_filter = ('type', 'season', 'num_arrows')


class ArcherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'middle_names', 'university', 'sex', 'experience')
    search_fields = ('first_name', 'last_name', 'middle_names')
    list_filter = ('sex', 'experience')


admin.site.register(Archer, ArcherAdmin)
admin.site.register(League, LeagueAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(LeagueSplit, LeagueSplitAdmin)
admin.site.register(Round, RoundAdmin)
