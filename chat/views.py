from django.shortcuts import render


def index(request):

    if not request.user.is_authenticated:
        print("Not Logged In!")
        return render(request, "chat/index.html", {})
    else:
        return render(request, "chat/home.html", {})

