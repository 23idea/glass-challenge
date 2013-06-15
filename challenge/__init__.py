from django.db.models.signals import post_save
from django.contrib.auth.models import User
import challenge.models as db


def create_user_callback(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        cu = db.Challenge_User(user=user)
        cu.save()

post_save.connect(create_user_callback, sender=User)
