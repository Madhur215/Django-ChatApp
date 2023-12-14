# utils.py
from .models import UserProfile

def get_user_id(username):
    use = UserProfile.objects.get(username=username)
    return use.id

def get_friends_list(user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
        ids = list(user.friends_set.all())
        friends = [UserProfile.objects.get(id=int(str(id))) for id in ids]
        return friends
    except UserProfile.DoesNotExist:
        return []
