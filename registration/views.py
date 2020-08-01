from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
# from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
# from main.models import Profile
#
#
# def SignUp(request):
#     message = []
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data.get('first_name')
#             last_name = form.cleaned_data.get('last_name')
#             phone_number = form.validate_phone()
#             email = form.validate_email()
#             username = form.validate_username()
#             password = form.validate_password()
#             if not email:
#                 message.append("Email already registered!")
#             elif not password:
#                 message.append("Passwords don't match!")
#             elif not username:
#                 message.append("Username already registered!")
#             elif not phone_number:
#                 message.append("Invalid phone number!")
#             else:
#                 print("SUCCESS!!!!!!")
#                 form.save()
#                 user = authenticate(username=username, password=password)
#                 login(request, user)
#                 profile = Profile(email=email, first_name=first_name, last_name=last_name, phone_number=phone_number)
#                 profile.save()
#                 return redirect("/profile")
#     else:
#         form = SignUpForm()
#     return render(request, "registration/signup.html", {"form": form, "heading": "Sign Up", "message": message})
#
