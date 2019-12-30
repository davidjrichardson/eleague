from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView


class DashboardIndexView(LoginRequiredMixin, TemplateView):
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'

    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        # TODO: Generate context data
        return super().get_context_data(**kwargs)


class UserProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/dashboard/login/'
    redirect_field_name = 'next'

    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        # TODO: Generate context data
        return super().get_context_data(**kwargs)
