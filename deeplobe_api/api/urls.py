from django.urls import path

# Create your urls here.
from .views import EmailAuthView, SocialAuthView, ForgotPasswordView


urlpatterns = [
    path("email-auth/", EmailAuthView.as_view(), name="email_authentication"),
    path("gmail-auth/", SocialAuthView.as_view(), name="social_authentication"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),

]
