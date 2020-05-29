from datetime import datetime, time, timedelta

from django import template
from django.utils import timezone
from django.template.defaultfilters import timeuntil

from league.models import LeagueSplit, LeagueEntry, ELeagueUser, League

register = template.Library()


@register.simple_tag(takes_context=True)
def entries_for_split(context, league: League, split: LeagueSplit):
    university = ELeagueUser.objects.get(user=context.request.user)
    return LeagueEntry.objects.for_league(league).for_split(split).for_club(university)


@register.filter()
def status(split: LeagueSplit, league: League) -> str:
    start_date = timezone.make_aware(datetime.combine(split.split_starts, time(0)))
    end_date = timezone.make_aware(datetime.combine(split.split_ends, time(0)))
    if timezone.now() < start_date and (start_date - timezone.now()) < timedelta(days=7):
        return f'Opens in {timeuntil(start_date, timezone.now())}'
    elif start_date <= timezone.now() < end_date:
        return "Open"
    elif (timezone.now() - end_date) > league.process_at:
        return "Published"
    else:
        return "Closed"
