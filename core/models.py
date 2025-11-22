from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователя"

    avatar = models.CharField(verbose_name="Аватар", max_length=255)
    name = models.CharField(verbose_name="Имя пользователя", max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f"#{self.id}: {self.name}"
