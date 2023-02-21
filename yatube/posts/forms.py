from .models import Post
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text", "group"]
        labels = {
            "text": "Текст на русском",
            "group": "Группа на русском",
        }
        help_texts = {
            "text": "Указывает текст",
            "group": "Указывает название группы",
        }
