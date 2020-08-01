from django.db import models


class UserProfile(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    friends = models.ManyToManyField('self', symmetrical=False, blank=True)

    def __str__(self):
        return f"{self.name}"


class Messages(models.Model):

    description = models.TextField()
    sender_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender_name')
    receiver_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver_name')
    time = models.TimeField()

    def __str__(self):
        return f"From: {self.sender_name}"

