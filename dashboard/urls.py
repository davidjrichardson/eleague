from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from dashboard.views import DashboardIndexView, UserProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name='dashboard_login'),
    path('logout/', LogoutView.as_view(), name='dashboard_logout'),
    path('reset/', LoginView.as_view(), name='dashboard_reset_pass'),
    path('profile/', UserProfileView.as_view(), name='dashboard_contact_info'),
    path('', DashboardIndexView.as_view(), name='dashboard_index')
]
