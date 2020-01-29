from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from dashboard.views import DashboardIndexView, UserProfileView, ChangePasswordView

urlpatterns = [
    path('password_reset/', PasswordResetView.as_view(), name='dashboard_password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='dashboard_password_reset_done'),
    path('reset/<uid>/<token>/', PasswordResetConfirmView.as_view(), name='dashboard_password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='dashboard_password_reset_complete'),
    path('login/', LoginView.as_view(), name='dashboard_login'),
    path('logout/', LogoutView.as_view(), name='dashboard_logout'),
    path('profile/', UserProfileView.as_view(), name='dashboard_contact_info'),
    path('profile/change_password/', ChangePasswordView.as_view(), name='dashboard_change_password'),
    path('', DashboardIndexView.as_view(), name='dashboard_index')
]
