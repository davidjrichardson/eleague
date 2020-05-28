from datetime import datetime, time

from django import template
from django.utils import timezone

from league.models import LeagueSplit, LeagueEntry, ELeagueUser, League

register = template.Library()


@register.simple_tag(takes_context=True)
def entries_for_split(context, league: League, split: LeagueSplit):
    university = ELeagueUser.objects.get(user=context.request.user)
    return LeagueEntry.objects.for_league(league).for_split(split).for_club(university)


@register.filter()
def status(split: LeagueSplit, league: League) -> str:
    if timezone.make_aware(datetime.combine(split.split_starts, time(0))) > timezone.now():
        return "Not open yet"
    elif timezone.make_aware(datetime.combine(split.split_starts, time(0))) <= timezone.now() < timezone.make_aware(
            datetime.combine(split.split_ends, time(0))):
        return "Open"
    # TODO: Have a way to show results are published
    else:
        return "Closed"
