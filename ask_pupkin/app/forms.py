from django import forms
from django.contrib.auth.models import User

from app.models import Answer, Question


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Password")

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Passwort")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Password again")
    avatar = forms.ImageField(required=False, label="Avatar")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password_confirm"):
            raise forms.ValidationError("Passwords not same!")
        return cleaned_data

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(label="Tags (example: tag1,tag2,...)", required=False)

    class Meta:
        model = Question
        fields = ['title', 'text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
