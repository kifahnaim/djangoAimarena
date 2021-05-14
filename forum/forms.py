from django import forms
from .models import Post, Userreg
from django.db import connection
from ckeditor.fields import RichTextField

class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control ', 'type': 'text', 'name': 'title', 'placeholder': 'Type the title'}))
    body = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control  ', 'type': 'text', 'name': 'body', 'placeholder': 'Type the body'}))
    author = forms.ModelChoiceField(
        queryset=Post.objects.order_by('author').values_list('author', flat=True).distinct())

    class Meta:
        model = Post
        fields = ('title', 'body', 'author')
        widgets = {
            'make_post' : RichTextField(),
        }



