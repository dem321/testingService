from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Answer


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class QuestionForm(forms.Form):
    question = forms.ModelChoiceField(queryset=Answer.objects.all(), required=True, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        question_id = kwargs.pop('question_id', None)
        super().__init__(*args, **kwargs)
        if question_id:
            self.fields['question'].queryset = Answer.objects.filter(question=question_id)
