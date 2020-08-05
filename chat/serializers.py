from rest_framework import serializers
from .models import Messages, UserProfile


class MessageSerializer(serializers.ModelSerializer):

    sender_name = serializers.SlugRelatedField(many=False, slug_field='username', queryset=UserProfile.objects.all())
    receiver_name = serializers.SlugRelatedField(many=False, slug_field='username', queryset=UserProfile.objects.all())

    class Meta:
        model = Messages
        fields = ['sender_name', 'receiver_name', 'description', 'time']

