from django.shortcuts import render, HttpResponse, redirect
from .models import UserProfile, Friends, Messages
from .network import client


def getFriendsList(id):
    try:
        user = UserProfile.objects.get(id=id)
        ids = list(user.friends_set.all())
        friends = []
        for id in ids:
            num = str(id)
            # print(type(num), num)
            fr = UserProfile.objects.get(id=int(num))
            friends.append(fr)
        return friends
    except:
        return []


def getUserId(username):
    use = UserProfile.objects.get(username=username)
    id = use.id
    return id


def index(request):

    if not request.user.is_authenticated:
        print("Not Logged In!")
        return render(request, "chat/index.html", {})
    else:
        username = request.user.username
        id = getUserId(username)
        friends = getFriendsList(id)
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

    username = request.user.username
    id = getUserId(username)
    friend = UserProfile.objects.get(username=name)
    curr_user = UserProfile.objects.get(id=id)
    print(curr_user.name)
    ls = curr_user.friends_set.all()
    flag = 0
    for username in ls:
        if username.friend == friend.id:
            flag = 1
            break
    if flag == 0:
        print("Friend Added!!")
        curr_user.friends_set.create(friend=friend.id)
    return redirect("/search")


def chat(request, username):
    friend = UserProfile.objects.get(username=username)
    id = getUserId(request.user.username)
    curr_user = UserProfile.objects.get(id=id)
    print("Name = ", curr_user)
    print("Friend ID = ", friend.id)
    ls = curr_user.messages_set.all()
    ls2 = friend.messages_set.all()
    msg_ls = []
    for items in ls:
        if items.receiver_name == friend.id:
            msg_ls.append(items)

    for items in ls2:
        if items.receiver_name == id:
            msg_ls.append(items)

    friends = getFriendsList(id)
    return render(request, "chat/chats.html", {'messages': msg_ls, 'friends': friends, 'id': id})
