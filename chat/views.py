from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, Messages
from django.views.generic import TemplateView
from .utils import get_friends_list, get_user_id
from .serializers import MessageSerializer, UserProfileSerializer
from .services import MessageService
from django.utils.decorators import method_decorator


from django.shortcuts import render
from django.views import View
from .models import UserProfile


class IndexView(View):
    def get(self, request):
        """
        Return the home page
        :param request:
        :return:
        """
        if not request.user.is_authenticated:
            print("Not Logged In!")
            return render(request, "chat/index.html", {})
        else:
            username = request.user.username
            id = get_user_id(username)
            friends = get_friends_list(id)
            return render(request, "chat/Base.html", {'friends': friends})


class FriendsListView(APIView):

    def get(self, request, id):
        """
        Get the list of friends of the user
        :param request:
        :param id: user id
        :return: list of friends
        """
        try:
            user = UserProfile.objects.get(id=id)
            ids = list(user.friends_set.all())
            friends = [UserProfile.objects.get(id=int(str(id))) for id in ids]
            return Response(friends)
        except UserProfile.DoesNotExist:
            return Response([])


class SearchView(TemplateView):
    template_name = "chat/search.html"

    def get(self, request, *args, **kwargs):
        users = list(UserProfile.objects.all().exclude(username=request.user.username))

        try:
            users = users[:10]
        except:
            users = users[:]

        id = get_user_id(request.user.username)
        friends = get_friends_list(id)

        return self.render_to_response({'users': users, 'friends': friends})

    def post(self, request, *args, **kwargs):
        query = request.data.get("search")
        users = [user for user in UserProfile.objects.all() if query in user.name or query in user.username]

        return self.render_to_response({'users': users})

    def post(self, request):
        """
        Search users based on a query
        :param request:
        :return:
        """
        query = request.data.get("search")
        users = [user for user in UserProfile.objects.all() if query in user.name or query in user.username]

        # Serialize UserProfile objects to dictionaries
        serialized_users = [UserProfileSerializer(user).data for user in users]

        return Response({'users': serialized_users})

    def get_user_id(self, username):
        use = UserProfile.objects.get(username=username)
        return use.id

    def get_friends_list(self, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
            ids = list(user.friends_set.all())
            friends = [UserProfile.objects.get(id=int(str(id))) for id in ids]
            return friends
        except UserProfile.DoesNotExist:
            return []


class AddFriendView(View):
    def get(self, request, name):
        """
        Add a user to the friend's list
        :param request:
        :param name:
        :return:
        """
        username = request.user.username
        id = get_user_id(username)
        friend = UserProfile.objects.get(username=name)
        curr_user = UserProfile.objects.get(id=id)

        ls = curr_user.friends_set.all()
        flag = 0
        for user in ls:
            if user.friend == friend.id:
                flag = 1
                break

        if flag == 0:
            print("Friend Added!!")
            curr_user.friends_set.create(friend=friend.id)
            friend.friends_set.create(friend=id)

        # Specify the URL to redirect to after adding a friend
        redirect_url = "/search/"
        return redirect(redirect_url)


class ChatView(APIView):

    def get(self, request, username):
        """
        Get the chat between two users.
        :param request:
        :param username:
        :return:
        """
        friend = UserProfile.objects.get(username=username)
        id = self.get_user_id(request.user.username)
        curr_user = UserProfile.objects.get(id=id)
        messages = Messages.objects.filter(sender_name=id, receiver_name=friend.id) | Messages.objects.filter(sender_name=friend.id, receiver_name=id)
        friends = self.get_friends_list(id)

        return render(request, "chat/messages.html",
                      {'messages': messages,
                       'friends': friends,
                       'curr_user': curr_user, 'friend': friend})

    def get_user_id(self, username):
        use = UserProfile.objects.get(username=username)
        return use.id

    def get_friends_list(self, user_id):
        try:
            user = UserProfile.objects.get(id=user_id)
            ids = list(user.friends_set.all())
            friends = [UserProfile.objects.get(id=int(str(id))) for id in ids]
            return friends
        except UserProfile.DoesNotExist:
            return []


# @method_decorator(csrf_exempt, name='dispatch')
# class MessageListView(APIView):
#
#     @csrf_exempt
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)
#
#     def get(self, request, sender=None, receiver=None):
#         """
#         Get the list of messages between two users.
#         :param request:
#         :param sender:
#         :param receiver:
#         :return:
#         """
#         messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
#         serializer = MessageSerializer(messages, many=True, context={'request': request})
#
#         for message in messages:
#             message.seen = True
#             message.save()
#
#         return JsonResponse(serializer.data, safe=False)

@method_decorator(csrf_exempt, name='dispatch')
class MessageListView(View):
    def get(self, request, sender=None, receiver=None):
        if sender is not None and receiver is not None:
            messages = Messages.objects.filter(sender_name=sender, receiver_name=receiver, seen=False)
            serializer = MessageSerializer(messages, many=True, context={"request": request})
            for message in messages:
                message.seen = True
                message.save()
            return JsonResponse(serializer.data, safe=False)

    def post(self, request, sender=None, receiver=None):
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            # Send a response message back to the sender
            response_message = "Your message was received successfully!"
            response_data = {'response_message': response_message}
            return JsonResponse(response_data, status=201)

        return JsonResponse(serializer.errors, status=400)


    def post(self, request, sender=None, receiver=None):
        """
        Create a new message.
        :param request:
        :param sender:
        :param receiver:
        :return:
        """
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Use the service to create the original message and automatic response
        original_message = MessageService.create_message_and_automatic_response(
            sender=serializer.validated_data['sender'],
            receiver=serializer.validated_data['receiver'],
            content=serializer.validated_data['content'],
        )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
