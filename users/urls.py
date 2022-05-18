from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('login/', CustomLoginView.as_view(
          redirect_authenticated_user=True, 
          template_name='users/login.html',
          authentication_form=LoginForm), 
          name='login'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
               template_name='users/password_reset_confirm.html'),
               name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
               template_name='users/password_reset_complete.html'),
               name='password_reset_complete'),

    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/edit', profile_edit, name='users-profile-edit'),
    path('profile/<user>/', profile_view, name='users-profile-view'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
