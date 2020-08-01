from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from chat.models import UserProfile


class SignUpForm(forms.Form):

    username = forms.CharField(min_length=5, max_length=20)
    name = forms.CharField(max_length=25, label="Name")
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def validate_username(self):
        username = self.cleaned_data['username']
        r = User.objects.filter(username=username)
        if r.count():
            return None
        return username

    def validate_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if not password1 or not password2:
            return None
        elif password2 != password1:
            return None
        return password1

    def validate_email(self):
        email = self.cleaned_data['email']
        r = UserProfile.objects.filter(email=email)
        if r.count():
            return None
        return email

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user


