from django.urls import path

# Create your urls here.
from .views import EmailAuthView, SocialAuthView


urlpatterns = [
    path("email-auth/", EmailAuthView.as_view(), name="email_authentication"),
    path("gmail-auth/", SocialAuthView.as_view(), name="social_authentication"),

]
