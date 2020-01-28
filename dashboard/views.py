from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from .models import ELeagueUser


class DashboardIndexView(LoginRequiredMixin, TemplateView):
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'

    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        # TODO: Generate context data
        return super().get_context_data(**kwargs)


class UserProfileView(LoginRequiredMixin, View):
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'

    template_name = 'dashboard/user_profile.html'

    success_url = '/dashboard/profile/'

    def get(self, request):
        context = {
            "email": request.user.email,
            # "form": ELeagueUserForm(instance=request.user),
            "university": ELeagueUser.objects.get(user=request.user).university
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        raise NotImplementedError
