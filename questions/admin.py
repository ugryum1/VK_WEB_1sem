from django.contrib import admin
from questions.models import Tag, Question, QuestionTag, Answer, AnswerTag, Like


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    search_fields = ['title']
    list_filter = ['created_at', 'updated_at']
    ordering = ['title']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'rating', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    search_fields = ['title', 'description']
    list_filter = ['created_at', 'updated_at', 'rating']
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'


@admin.register(QuestionTag)
class QuestionTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'tag', 'created_at', 'updated_at']
    list_display_links = ['id', 'question']
    list_filter = ['created_at', 'updated_at']
    raw_id_fields = ['question', 'tag']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'truncated_text', 'question', 'user', 'rating', 'is_accepted', 'created_at']
    list_display_links = ['id', 'truncated_text']
    search_fields = ['text', 'question__title']
    list_filter = ['is_accepted', 'created_at', 'updated_at', 'rating']
    raw_id_fields = ['question', 'user']
    date_hierarchy = 'created_at'

    def truncated_text(self, obj):
        """Обрезает длинный текст ответа для отображения в списке"""
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    truncated_text.short_description = 'Текст ответа'


@admin.register(AnswerTag)
class AnswerTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'answer', 'tag', 'created_at', 'updated_at']
    list_display_links = ['id', 'answer']
    list_filter = ['created_at', 'updated_at']
    raw_id_fields = ['answer', 'tag']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'get_target', 'weight', 'created_at']
    list_display_links = ['id', 'user']
    list_filter = ['weight', 'created_at', 'updated_at']
    raw_id_fields = ['user', 'question', 'answer']

    def get_target(self, obj):
        """Показывает на что поставлен лайк/дизлайк"""
        if obj.question:
            return f"Вопрос: {obj.question.title}"
        elif obj.answer:
            question_title = obj.answer.question.title
            short_title = question_title[:50] + '...' if len(question_title) > 50 else question_title
            return f"Ответ на: {short_title}"
        return "Неизвестно"
    get_target.short_description = 'Объект'
