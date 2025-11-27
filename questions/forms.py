from django import forms
from django.core.exceptions import ValidationError
from .models import Answer, Question, Tag, QuestionTag


class AnswerForm(forms.Form):
    text = forms.CharField(
        label="Ваш ответ",
        widget=forms.Textarea(attrs={
            "class": "answer-textarea",
            "placeholder": "Введите ваш ответ здесь...",
            "rows": "6",
            "id": "answer-text"
        })
    )


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)


    def clean_text(self):
        text = self.cleaned_data["text"]
        if len(text.strip()) < 10:
            raise ValidationError("Ответ должен содержать минимум 10 символов")
        return text


    def save(self):
        text = self.cleaned_data["text"]
        answer = Answer.objects.create(
            question=self.question,
            text=text,
            user=self.user,
            rating=0
        )
        return answer


class QuestionForm(forms.Form):
    title = forms.CharField(
        label="Название",
        max_length=200,
        widget=forms.Textarea(attrs={
            "class": "form-input",
            "placeholder": "Введите заголовок вопроса",
            "id": "question-title"
        })
    )
    description = forms.CharField(
        label="Текст вопроса",
        widget=forms.TextInput(attrs={
            "class": "form-textarea",
            "placeholder": "Опишите подробно ваш вопрос",
            "rows": "8",
            "id": "question-text"
        })
    )
    tags = forms.CharField(
        label="Теги",
        widget=forms.TextInput(attrs={
            "class": "form-input",
            "placeholder": "python, django, postgresql",
            "id": "question-tags"
        })
    )


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title.strip()) < 3:
            raise ValidationError("Заголовок должен содержать минимум 3 символа")
        return title


    def clean_description(self):
        description = self.cleaned_data["description"]
        if len(description.strip()) < 20:
            raise ValidationError("Текст вопроса должен содержать минимум 20 символов")
        return description


    def clean_tags(self):
        tags = self.cleaned_data["tags"]
        if not tags.strip():
            raise ValidationError("Укажите хотя бы один тег")

        tag_list = [tag.strip().lower() for tag in tags.split(",") if tag.strip()]

        if len(tag_list) == 0:
            raise ValidationError("Укажите хотя бы один тег")

        if len(tag_list) > 5:
            raise ValidationError("Можно указать не более 5 тегов")

        return tag_list


    def save(self):
        title = self.cleaned_data["title"]
        description = self.cleaned_data["description"]
        tag_list = self.cleaned_data["tags"]

        question = Question.objects.create(
            title=title,
            description=description,
            user=self.user,
            rating=0,
        )

        for tag_name in tag_list:
            tag, _ = Tag.objects.get_or_create(title=tag_name)
            QuestionTag.objects.create(question=question, tag=tag)

        return question
