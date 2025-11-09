from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    title = models.CharField(verbose_name="Название тега", max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id}: {self.title}"


class Question(models.Model):
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    title = models.CharField(verbose_name="Заголовок вопроса", max_length=200)
    description = models.TextField(verbose_name="Описание вопроса")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name="Рейтинг", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id}: {self.title}"


class QuestionTag(models.Model):
    class Meta:
        verbose_name = "Тег вопроса"
        verbose_name_plural = "Теги вопросов"

    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, verbose_name="Тег", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id}: {self.question.title} - {self.tag.title}"


class Answer(models.Model):
    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE, related_name="answers")
    text = models.TextField(verbose_name="Текст ответа")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    rating = models.IntegerField(verbose_name="Рейтинг", default=0)
    is_accepted = models.BooleanField(verbose_name="Принятый ответ", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id}: Ответ на '{self.question.title}'"


class AnswerTag(models.Model):
    class Meta:
        verbose_name = "Тег ответа"
        verbose_name_plural = "Теги ответов"

    answer = models.ForeignKey(Answer, verbose_name="Ответ", on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, verbose_name="Тег", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id}: {self.answer.question.title} - {self.tag.title}"


class Like(models.Model):
    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        constraints = [
            models.CheckConstraint(
                check=models.Q(question__isnull=False) | models.Q(answer__isnull=False),
                name='like_has_question_or_answer'
            ),
            models.UniqueConstraint(
                fields=['user', 'question'],
                condition=models.Q(question__isnull=False),
                name='unique_user_question_like'
            ),
            models.UniqueConstraint(
                fields=['user', 'answer'],
                condition=models.Q(answer__isnull=False),
                name='unique_user_answer_like'
            )
        ]

    WEIGHT_CHOICES = [
        (1, 'Лайк'),
        (-1, 'Дизлайк'),
    ]

    weight = models.IntegerField(verbose_name="Вес", choices=WEIGHT_CHOICES, default=1)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, verbose_name="Ответ", on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        target = self.question.title if self.question else self.answer.question.title
        action = "Лайк" if self.weight == 1 else "Дизлайк"
        return f"#{self.id}: {action} на '{target}'"
