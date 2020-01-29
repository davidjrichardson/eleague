from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

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
    custom_help_labels = ['Your password must contain at least 8 alphanumeric characters.']

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
