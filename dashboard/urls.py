from django.urls import path

from dashboard.views import DashboardLoginView, DashboardIndexView

urlpatterns = [
    path('login/', DashboardLoginView.as_view(), name='dashboard_login'),
    path('', DashboardIndexView.as_view(), name='dashboard_index')
]
