from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    # вопросы с пользователем, тегами и количеством ответов
    def with_related_data(self):
        return self.get_queryset().select_related('user').prefetch_related(
            'question_tags__tag'
        ).annotate(
            answers_count=models.Count('answers')
        )


    # лучшие вопросы по рейтингу
    def top_questions(self):
        return self.with_related_data().order_by('-rating')


    # вопросы по тегу
    def by_tag(self, tag):
        return self.with_related_data().filter(question_tags__tag=tag).distinct()


class TagManager(models.Manager):
    # топ тегов
    def top_tags(self):
        return self.get_queryset().annotate(
            question_count=models.Count('questiontag__question')
        ).order_by('-question_count')[:7]


class AnswerManager(models.Manager):
    # ответы для конкретного вопроса
    def for_question(self, question):
        return self.filter(question=question).select_related('user').order_by('-rating')


class UserManager(models.Manager):
    # топ пользователей
    def top_users(self):
        return self.get_queryset().annotate(
            question_count=models.Count('question')
        ).order_by('-question_count')[:3]


class Tag(models.Model):
    objects = TagManager()

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    title = models.CharField(verbose_name="Название тега", max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id}: {self.title}"


class Question(models.Model):
    objects = QuestionManager()

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

    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE,
                                 related_name="question_tags")
    tag = models.ForeignKey(Tag, verbose_name="Тег", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"#{self.id}: {self.question.title} - {self.tag.title}"


class Answer(models.Model):
    objects = AnswerManager()

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


# кастомный менеджер для User модели
User.add_to_class('objects', UserManager())
