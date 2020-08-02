from django.shortcuts import render, HttpResponse, redirect
from .models import UserProfile, Friends, Messages


def getFriendsList(id):

    user = UserProfile.objects.get(id=id)
    ids = list(user.friends_set.all())
    friends = []
    for id in ids:
        num = str(id)
        # print(type(num), num)
        fr = UserProfile.objects.get(id=int(num))
        friends.append(fr)
    return friends


def index(request):

    if not request.user.is_authenticated:
        print("Not Logged In!")
        return render(request, "chat/index.html", {})
    else:
        friends = getFriendsList(request.user.id)
        return render(request, "chat/Base.html", {'friends': friends})


def search(request):
    users = list(UserProfile.objects.all())
    for user in users:
        if user.username == request.user.username:
            users.remove(user)
            break

    if request.method == "POST":
        print("SEARCHING!!")
        query = request.POST.get("search")
        user_ls = []
        for user in users:
            if query in user.name or query in user.username:
                user_ls.append(user)
        return render(request, "chat/search.html", {'users': user_ls, })

    try:
        users = users[:10]
    except:
        users = users[:]
    friends = getFriendsList(request.user.id)
    return render(request, "chat/search.html", {'users': users, 'friends': friends})


def addFriend(request, name):

    id = request.user.id
    friend = UserProfile.objects.get(username=name)
    curr_user = UserProfile.objects.get(id=id)
    print(curr_user.name)
    ls = curr_user.friends_set.all()
    flag = 0
    for username in ls:
        if username.id == friend.id:
            flag = 1
    if flag == 0:
        print("Friend Added!!")
        curr_user.friends_set.create(friend=friend.id)
    return redirect("/search")
