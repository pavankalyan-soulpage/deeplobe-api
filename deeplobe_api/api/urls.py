from django.urls import path

# Create your urls here.
<<<<<<< HEAD
from .views import (
    EmailAuthView,
    SocialAuthView,
    ForgotPasswordView,
    ForgotPasswordConfirmView,
    ClassificationImageUpload,
    UserView,
    UserDetail,
)
=======
from .views import EmailAuthView, SocialAuthView, ForgotPasswordView, ForgotPasswordConfirmView, ClassificationImageUpload, UserCreate, UserDetail, TaggingImageUpload

>>>>>>> dee23649214241b4a394ebf0ae85fc6ccfc9016f


urlpatterns = [
    path("email-auth/", EmailAuthView.as_view(), name="email_authentication"),
    path("gmail-auth/", SocialAuthView.as_view(), name="social_authentication"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
<<<<<<< HEAD
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
=======
    path("password-confirm/", ForgotPasswordConfirmView.as_view(), name="confirm_password"),
    path("classification-upload/<str:category_name>/", ClassificationImageUpload.as_view(), name="classification_upload"),
    path("users/", UserCreate.as_view(), name="create"),
    path("users/<int:pk>/", UserDetail.as_view(), name="retreive user"),
    path("tagging-upload/", TaggingImageUpload.as_view(), name="tagging_upload"),
>>>>>>> dee23649214241b4a394ebf0ae85fc6ccfc9016f
]
