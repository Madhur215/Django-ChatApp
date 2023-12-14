# from django.urls import path, include
# from . import views
#
# urlpatterns = [
#     path("", views.index, name="index"),
#     path("search/", views.search, name="search"),
#     path("add-friend/<str:name>", views.addFriend, name="add-friend"),
#     path("chat/<str:username>", views.chat, name="chat"),
#     path('api/messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),
#     path('api/messages', views.message_list, name='message-list'),
# ]

from django.urls import path
from chat.views import (
    FriendsListView,
    SearchView,
    AddFriendView,
    ChatView,
    MessageListView,
    IndexView,
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', SearchView.as_view(), name='search'),
    path('friends/<int:id>/', FriendsListView.as_view(), name='friends-list'),
    path('add-friend/<str:name>/', AddFriendView.as_view(), name='add-friend'),
    path('chat/<str:username>/', ChatView.as_view(), name='chat'),
    path('api/messages/<str:sender>/<str:receiver>/', MessageListView.as_view(), name='message-detail'),
    path('api/messages', MessageListView.as_view(), name='message-list'),
]


