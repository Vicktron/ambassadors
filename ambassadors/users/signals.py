from .models import Account, Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, *args, **kwargs):
    if created:
        Account.objects.create(user=instance)
        

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    

@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    instance.account.save()