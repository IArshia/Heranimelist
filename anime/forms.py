from django import forms
from .models import Comment, ListAnime, ListAnimeItem


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('user', 'anime', 'content')
        widgets = {
            'user':forms.HiddenInput(),
            'anime':forms.HiddenInput(),
        }


class ListAnimeForm(forms.ModelForm):
    class Meta:
        model = ListAnime
        fields = ('user', 'name')
        widgets = {
            'user':forms.HiddenInput(),
        }