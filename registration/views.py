from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from chat.models import UserProfile


def SignUp(request):
    """
    Sign up view
    :param request:
    :return:
    """
    message = []
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.validate_email()
            username = form.validate_username()
            password = form.validate_password()
            if not email:
                message.append("Email already registered!")
            elif not password:
                message.append("Passwords don't match!")
            elif not username:
                message.append("Username already registered!")
            else:
                print("SUCCESS!!!!")
                form.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                profile = UserProfile(email=email, name=name, username=username)
                profile.save()
                return redirect("/")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form, "heading": "Sign Up", "message": message})

