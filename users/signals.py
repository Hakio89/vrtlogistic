from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from vrtlogistic.settings import EMAIL_HOST_USER
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

# Automatically create a profile for new users
@receiver(post_save, sender=User)
def create_profile_on_user_save(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(owner=instance)

# Automatically create a profile for existing users when they log in
@receiver(user_logged_in)
def create_profile_on_login(sender, user, request, **kwargs):
    Profile.objects.get_or_create(owner=user)

#@receiver(post_save, sender=Profile) - jedna z metod wywoływania sygnałów

def profileCreated(sender, created, instance, **kwargs):
    print('Profile created successfully')
    profile = instance
    owner = profile.owner.username
    email = profile.owner.email
    
    subject = 'Witamy w Virtual Logistic'
    message_text = f'Cześć {owner},\n\
        Zostało dla ciebie utworzone nowe konto użytkownika\n\
        Zaloguj się na stronie: virtuallogistic/users/login/ \n\
        Pozdrawiamy\n\
        Zespół Virtual Logistic'
    
    send_mail(
        subject,
        message_text,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
        )
        
post_save.connect(profileCreated, sender=Profile, weak=False)