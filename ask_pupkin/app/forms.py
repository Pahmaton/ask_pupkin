from django import forms
from django.contrib.auth.models import User

from app.models import Answer, Question


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Password")

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Repeat Password"
    )
    avatar = forms.ImageField(
        required=False,
        label="Avatar",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data.get("password")
        pass2 = cleaned_data.get("password_confirm")

        if pass1 and pass2 and pass1 != pass2:
            self.add_error('password_confirm', "Passwords do not match!")

        return cleaned_data

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(label="Tags (example: tag1,tag2,...)", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Question
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
