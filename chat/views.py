from django.shortcuts import render, HttpResponse, redirect
from .models import UserProfile, Friends, Messages
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from chat.serializers import MessageSerializer


def getFriendsList(id):
    try:
        user = UserProfile.objects.get(id=id)
        ids = list(user.friends_set.all())
        friends = []
        for id in ids:
            num = str(id)
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
    id = getUserId(request.user.username)
    friends = getFriendsList(id)
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
        friend.friends_set.create(friend=id)
    return redirect("/search")


def sortByTime(msg_ls):
    cnt = 0
    for i in range(len(msg_ls)):
        min_ind = i
        for j in range(i + 1, len(msg_ls)):
            if msg_ls[min_ind].time > msg_ls[j].time:
                min_ind = j
        msg_ls[i], msg_ls[min_ind] = msg_ls[min_ind], msg_ls[i]
        cnt += 1
        if cnt >= 10:
            return msg_ls[:10]
    return msg_ls


def chat(request, username):
    friend = UserProfile.objects.get(username=username)
    id = getUserId(request.user.username)
    curr_user = UserProfile.objects.get(id=id)
    print("Name = ", curr_user)
    print("Friend ID = ", friend.id)

    friends = getFriendsList(id)
    return render(request, "chat/messages.html",
                  {'messages': Messages.objects.filter(sender_name=id, receiver_name=friend.id) |
                               Messages.objects.filter(sender_name=friend.id, receiver_name=id),
                   'friends': friends,
                   'curr_user': curr_user, 'friend': friend})


@csrf_exempt
def message_list(request, sender=None, receiver=None):

    if request.method == 'GET':
        messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.seen = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
