from django import forms 
from .models import Comment

class Commentform(forms.ModelForm):
    class Meta:
        model=Comment
        exclude=['post']
        labels={
            'user_name':'your name',
            'user_email':'your email',
            'text':'your text'
        }