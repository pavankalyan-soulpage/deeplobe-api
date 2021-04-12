from django.db import models
from ..mixins import TimeAuditModel
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("email must give")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeAuditModel):

    username = models.CharField(max_length=255, blank=True)

    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=255)

    last_name = models.CharField(max_length=255)

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    company = models.CharField(max_length=255)

    job_title = models.CharField(max_length=255)

    terms_conditions = models.BooleanField(default=False)

    token = models.CharField(max_length=256, null=True, blank=True)

    token_status = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username","password"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "users"







