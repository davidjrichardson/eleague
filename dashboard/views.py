from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView


class DashboardIndexView(LoginRequiredMixin, TemplateView):
    login_url = '/dashboard/login/'
    redirect_field_name = 'redirect_to'

    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        # TODO: Generate context data
        return super().get_context_data(**kwargs)


class DashboardLoginView(View):
    template_name = 'dashboard/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard_index')

        # TODO: Generate the context
        return render(request, template_name=self.template_name)

    def post(self, request):
        # TODO: Sign the user in if the credentials are correct
        return render(request, template_name=self.template_name)
