from django import forms
from django.core.exceptions import ValidationError
from .models import Answer
import re


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
