from django.contrib.auth.views import LoginView
from django.urls import path

from dashboard.views import DashboardIndexView

urlpatterns = [
    path('login/', LoginView.as_view(), name='dashboard_login'),
    path('', DashboardIndexView.as_view(), name='dashboard_index')
]
