from django.urls import path

# Create your urls here.
from .views import (
    EmailAuthView,
    SocialAuthView,
    ForgotPasswordView,
    ForgotPasswordConfirmView,
    ClassificationImageUpload,
    UserView,
    UserDetail,
)


urlpatterns = [
    path("email-auth/", EmailAuthView.as_view(), name="email_authentication"),
    path("gmail-auth/", SocialAuthView.as_view(), name="social_authentication"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path(
        "password-confirm/",
        ForgotPasswordConfirmView.as_view(),
        name="confirm_password",
    ),
    path(
        "classification-upload/",
        ClassificationImageUpload.as_view(),
        name="classification_upload",
    ),
    path("users/", UserView.as_view(), name="create"),
    path("users/<int:pk>/", UserDetail.as_view(), name="retreive user"),
]
