from django.db import models
from django.contrib.auth.models import User


class UserProfileManager(models.Manager):
    def top_users(self, limit=3):
        return self.get_queryset().annotate(
            question_count=models.Count('user__question')
        ).order_by('-question_count')[:limit]


class UserProfile(models.Model):
    objects = UserProfileManager()

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
