from django.shortcuts import render


def index(request):

    if not request.user.is_authenticated:
        print("Not Logged In!")
        return render(request, "chat/index.html", {})
    else:
        return render(request, "chat/home.html", {})


def search(request):
    return render(request, "chat/search.html", {})
