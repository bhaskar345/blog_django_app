from django import forms
from django.db import models
from .models import Comments

class Mailform(forms.Form):
    name=forms.CharField()
    email=forms.EmailField()
    to=forms.EmailField()

class CommentsForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields=['name','email','body']
