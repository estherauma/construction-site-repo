from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.utils.timezone import now
from django.contrib.auth.models import User
# from .models import Profile
from django.db.models.signals import post_save

@receiver(user_logged_in)
def log_login_user(sender, request, user, **kwargs):
    # user.last_login = now()
    # user.profile.last_login_ip = request.META.get('REMOTE_ADDR')
    # user.profile.last_login_time = now()
    # user.profile.save()
    print('User looged in')


@receiver(user_login_failed)
def log_login_user_failed(sender, credentials, request, **kwargs):
    print("User failed to login")

@receiver(user_logged_out)
def log_logout_user(sender, request, user, **kwargs):
    print("User logged out")

# @receiver(post_save, sender=User)
# def create_or_update_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()