from django.db import models


class UserProfile(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name}"


class Messages(models.Model):

    description = models.TextField()
    # receiver_name = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='receiver_name')
    time = models.TimeField()
    receiver_name = models.IntegerField()

    def __str__(self):
        return f"From: {self.receiver_name}"


class Friends(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    friend = models.IntegerField()

    def __str__(self):
        return f"{self.friend}"

