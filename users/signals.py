from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Admin , Professional

from django.core.mail import send_mail
from django.conf import settings

def createAdmin(sender, instance, created, **kwargs):
    if created:
        profile = instance
        user = User.objects.create(
                username = profile.username,
                first_name = profile.prenom,
                last_name = profile.nom,
                email = profile.email,
                is_superuser = True,
                is_staff = False,
            )
        host = "http://127.0.0.1:8000"
        
        subject = '👋 Salutations de COPDiag!'
        message = "Bienvenue, "+profile.username+".\n\n Nous sommes heureux que vous soyez ici. Ensemble, avec des gens comme vous, nous aidons les patients à obtenir des diagnostics médicaux avec une grande précision. \n\n Pour pouvoir vous connecter à notre site Web, veuillez réinitialiser votre mot de passe en suivant le lien ci-dessous: \n\n👉 "+host+reverse_lazy('reset_password')+" "

        email_sender = settings.EMAIL_HOST_USER
        print(message)
        send_mail(
            subject,
            message,
            email_sender,
            [profile.email],
            fail_silently=False,
        )
        profile.user = user
        profile.save()

def updateAdmin(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    
    if created == False:
        user.first_name = profile.prenom
        user.last_name = profile.nom
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleteAdmin(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass



def createStaff(sender, instance, created, **kwargs):
    if created:
        profile = instance
        user = User.objects.create(
                username = profile.username,
                first_name = profile.prenom,
                last_name = profile.nom,
                email = profile.email,
                is_superuser = False,
                is_staff = True,
            )
        host = "http://127.0.0.1:8000"
        
        subject = '👋 Salutations de COPDiag!'
        message = "Bienvenue, "+profile.username+".\n\n Nous sommes heureux que vous soyez ici. Ensemble, avec des gens comme vous, nous aidons les patients à obtenir des diagnostics médicaux avec une grande précision. \n\n Pour pouvoir vous connecter à notre site Web, veuillez réinitialiser votre mot de passe en suivant le lien ci-dessous: \n\n👉 "+host+reverse_lazy('reset_password')+" "

        email_sender = settings.EMAIL_HOST_USER
        print(message)
        send_mail(
            subject,
            message,
            email_sender,
            [profile.email],
            fail_silently=False,
        )
        profile.user = user
        profile.save()

def updateStaff(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    
    if created == False:
        user.first_name = profile.prenom
        user.last_name = profile.nom
        user.username = profile.username
        user.email = profile.email
        user.save()

def deleteStaff(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass




post_save.connect(createAdmin, sender=Admin)
post_save.connect(updateAdmin, sender=Admin)
post_delete.connect(deleteAdmin, sender=Admin)

post_save.connect(createStaff, sender=Professional)
post_save.connect(updateStaff, sender=Professional)
post_delete.connect(deleteStaff, sender=Professional)
