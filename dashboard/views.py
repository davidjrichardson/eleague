import sys

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, Page
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView

from league.models import League, Archer
from .models import ELeagueUser


def get_archers(request, university: ELeagueUser) -> (Page, int):
    archers = Archer.objects.filter(university=university).order_by('last_name', 'first_name', 'middle_names').all()

    page_number = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)

    if per_page == 'all':
        paginator = Paginator(archers, per_page=sys.maxsize)
    else:
        paginator = Paginator(archers, per_page=per_page)
    return paginator.get_page(page_number), len(archers)


class DashboardArchersPaginatorView(LoginRequiredMixin, View):
    template_name = 'dashboard/partials/archers_list.html'

    def get(self, request):
        # TODO: Paginate the archers list
        context = {}

        return render(request, self.template_name, context=context)


class DashboardIndexView(LoginRequiredMixin, TemplateView):
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'

    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        # TODO: Generate context data
        context = super().get_context_data(**kwargs)

        university = ELeagueUser.objects.get(user=self.request.user)
        leagues = League.objects.filter(start_at__lte=timezone.now(), end_at__gt=timezone.now()).order_by(
            'start_at').all()
        archers, num_archers = get_archers(self.request, university)

        context.update({
            "university": university.university,
            "leagues": leagues,
            "archers": archers,
            "num_archers": num_archers
        })
        return context


class UserProfileView(LoginRequiredMixin, View):
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'

    template_name = 'dashboard/user_profile.html'

    success_url = '/dashboard/profile/'

    def get(self, request):
        context = {
            "email": request.user.email,
            "university": ELeagueUser.objects.get(user=request.user).university
        }

        return render(request, self.template_name, context=context)


class ChangePasswordView(LoginRequiredMixin, View):
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'

    success_url = '/dashboard/profile/'

    template_name = 'dashboard/partials/change_password.html'
    custom_help_labels = 'Your password must contain at least 8 alphanumeric characters.'

    def get(self, request):
        context = {
            "form": PasswordChangeForm(request.user),
            "university": ELeagueUser.objects.get(user=request.user).university,
            "custom_help_labels": self.custom_help_labels
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')

            return redirect('dashboard_change_password')
        else:
            messages.error(request, 'Please correct the error(s) below.', extra_tags='danger')

            context = {
                "form": form,
                "university": ELeagueUser.objects.get(user=request.user).university,
                "custom_help_labels": self.custom_help_labels
            }

            return render(request, self.template_name, context=context)
