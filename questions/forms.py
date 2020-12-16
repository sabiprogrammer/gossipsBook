from PIL import Image
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Questions


class AddQuestionsForm(forms.ModelForm):
    OPTIONS = (
        ('questions', 'questions'),
        ('gossips', 'Gossips'),
        ('cheaters', 'cheaters'),
    )

    tags = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={
        'class': 'form-check form-check-inline remove_bullet'
    }), choices=OPTIONS)

    class Meta:
        model = Questions
        fields = ['title', 'content', 'image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Question title',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your question to the community',
            }),
            }


