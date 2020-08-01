from django.db import models


class UserProfile(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name}"


class Messages(models.Model):

    description = models.TextField()
    sender_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender_name')
    receiver_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver_name')
    time = models.TimeField()

    def __str__(self):
        return f"From: {self.sender_name}"


class Friends(models.Model):

    friend1 = models.ForeignKey(UserProfile, related_name="friend1", on_delete=models.CASCADE)
    friend2 = models.ForeignKey(UserProfile, related_name='friend2', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.friend1} & {self.friend2}"

