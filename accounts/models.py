from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password, check_password


# 1️⃣ Custom User Manager
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email აუცილებელია")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser უნდა იყოს is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser უნდა იყოს is_superuser=True")

        return self.create_user(email, password, **extra_fields)


# 2️⃣ Custom User Model
class User(AbstractUser):
    username = None  # username აღარ გვჭირდება
    email = models.EmailField("email address", unique=True)
    bio = models.TextField(blank=True)
    profile_image = models.URLField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    recovery_question = models.CharField(max_length=255, blank=True, null=True)
    _recovery_answer = models.CharField(max_length=128, blank=True, null=True)

    USERNAME_FIELD = "email"  # email იქნება მთავარი იდენტიფიკატორი
    REQUIRED_FIELDS = []  # სხვა ველები საჭირო არაა

    objects = CustomUserManager()  # აუცილებელია create_user / create_superuser

    def set_recovery_answer(self, raw):
        if raw:
            self._recovery_answer = make_password(raw)
        else:
            self._recovery_answer = None

    def check_recovery_answer(self, raw):
        if not self._recovery_answer:
            return False
        return check_password(raw, self._recovery_answer)

    def __str__(self):
        return self.email
