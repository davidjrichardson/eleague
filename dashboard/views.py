from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import password_validators_help_texts
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.forms import PasswordChangeForm


from .models import ELeagueUser


class DashboardIndexView(LoginRequiredMixin, TemplateView):
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'

    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        # TODO: Generate context data
        context = super().get_context_data(**kwargs)

        context.update({
            "university": ELeagueUser.objects.get(user=self.request.user).university
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
            # "form": ELeagueUserForm(instance=request.user),
            "university": ELeagueUser.objects.get(user=request.user).university
        }

        return render(request, self.template_name, context=context)


class ChangePasswordView(LoginRequiredMixin, View):
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'

    success_url = '/dashboard/profile/'

    template_name = 'dashboard/change_password.html'

    def get(self, request):
        context = {
            "form": PasswordChangeForm(request.user),
            "university": ELeagueUser.objects.get(user=request.user).university,
            "custom_help_labels": ['Your password must contain at least 8 alphanumeric characters.']
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        raise NotImplementedError
