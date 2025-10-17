from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class User(AbstractUser):
    username = None  # we will use email as identifier
    email = models.EmailField('email address', unique=True)
    bio = models.TextField(blank=True)
    profile_image = models.URLField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # at least one verified contact
    recovery_question = models.CharField(max_length=255, blank=True, null=True)
    _recovery_answer = models.CharField(max_length=128, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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
