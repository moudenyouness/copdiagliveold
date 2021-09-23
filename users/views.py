from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Professional , Patient , Admin , Message 
from .forms import MessageForm, CustomPatientCreationForm, CustomStaffCreationForm  , CustomAdminCreationForm
from base.models import Contact
from django.db.models import Q
from .utils import paginateObjects , predictResult

from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def loginUser(request):
    usertype = None

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    usertype = "Admin"
                    return redirect(request.GET['next'] if 'next' in request.GET else 'admins') #
                elif user.is_staff:
                    usertype = "Staff"
                    return redirect(request.GET['next'] if 'next' in request.GET else 'staffs') #

            else:
                messages.error(request, "Nom d'utilisateur ou Mot de passe est incorrect")
        except:
            messages.add_message(request, messages.ERROR, "Nom d'utilisateur n'exist pas")
        
   
    context = {'usertype': usertype}
    return render(request, 'users/login.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, "Vous êtes maintenant déconnecté!")
    return redirect('login')



@login_required(login_url = 'login')
def AdminsPage(request):
    utilisateur = request.user
    admins = Admin.objects.all()

    context = {'admins': admins, 'utilisateur': utilisateur}
    return render(request, 'users/index.html', context)


@login_required(login_url = 'login')
def StaffsPage(request):
    staffs = Professional.objects.all()

    context = {'staffs': staffs}
    return render(request, 'users/staffs.html', context)


@login_required(login_url = 'login')
def PatientsPage(request):
    patients = None
    results = 10
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    if request.user.is_superuser:
        patients = Patient.objects.all()
    else:
        usr = request.user.professional
        patients = usr.patient_set.all()


    patients = patients.distinct().filter(
        Q(prenom__icontains=search_query) | 
        Q(nom__icontains=search_query) | 
        Q(cin__icontains=search_query) | 
        Q(email__icontains=search_query) | 
        Q(age__icontains=search_query) | 
        Q(phone__icontains=search_query) | 
        Q(gender__icontains=search_query) | 
        Q(location__icontains=search_query) | 
        Q(staff__nom__icontains=search_query) | 
        Q(staff__prenom__icontains=search_query) 
        )

    custom_range, patients = paginateObjects(request, patients, results)
    

    context = {'patients': patients, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'users/patients.html', context)



@login_required(login_url = 'login')
def viewPatient(request, pk):
    patient = None

    if Patient.objects.get(id=pk):
        patient = Patient.objects.get(id=pk)
    
    context = {'patient': patient}
    return render(request, 'users/patient.html', context)



@login_required(login_url = 'login')
def userProfile(request, pk):
    profile = None
    usr = None
    patients = None
    try:
        if Admin.objects.get(id=pk):
            profile = Admin.objects.get(id=pk)
    except:
        if Professional.objects.get(id=pk):
            profile = Professional.objects.get(id=pk)
            patients = profile.patient_set.all()
    
    if request.user.is_superuser:
        usr = request.user.admin.id
    elif request.user.is_staff:
        usr = request.user.professional.id
            
    
    context = {'profile': profile, 'usr': usr, 'patients': patients}
    return render(request, 'users/profile.html', context)


@login_required(login_url = 'login')
def userAccount(request):
    profile = None

    if request.user.is_superuser:
        profile = request.user.admin
        
    if request.user.is_staff and request.user.is_superuser == False:
        profile = request.user.professional
        
    context = {'profile': profile}
    return render(request, 'users/account.html', context)


@login_required(login_url = 'login')
def editAccount(request):
    page = 'update'
    
    usrn = request.user.username
    profile = Admin.objects.get(username=usrn)
    
    form = CustomAdminCreationForm(instance=profile)

    if request.method == 'POST':
        form = CustomAdminCreationForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.prenom = profile.prenom.capitalize()
            profile.nom = profile.nom.capitalize()
            profile.cin = profile.cin.upper()
            profile.username = profile.username.lower()
            profile.email = profile.email.lower()
            if usrn == profile.username:
                profile.save()

                messages.success(request, "Le compte a été mis à jour avec succès!")
                return redirect('account')
            else:
                try:
                    User.objects.get(username=profile.username)
                    messages.error(request, "Veuillez utiliser un autre nom d'utilisateur")
                except:
                    profile.save()

                    messages.success(request, "Le compte a été mis à jour avec succès!")
                    return redirect('account')

        else:
            messages.error(request, "Une erreur s'est produite lors de la modification du compte!")
    
    context = {'page': page, 'form': form}
    return render(request, 'users/user_form.html', context)


@login_required(login_url = 'login')
def createAdmin(request):
    if request.user.is_superuser:
        page = 'create'
        form = CustomAdminCreationForm()

        if request.method == 'POST':
            form = CustomAdminCreationForm(request.POST)
            if form.is_valid():
                admin = form.save(commit=False)
                admin.prenom = admin.prenom.capitalize()
                admin.nom = admin.nom.capitalize()
                admin.cin = admin.cin.upper()
                admin.username = admin.username.lower()
                admin.email = admin.email.lower()
                try:
                    User.objects.get(username=admin.username)
                    messages.error(request, "Veuillez utiliser un autre nom d'utilisateur!")
                except:
                    admin.save()

                    messages.success(request, "L'administrateur a été créé avec succès!")
                    return redirect('admins')

            else:
                messages.error(request, "Une erreur s'est produite lors de la création du compte!")
    else:
        return redirect('admins')
    
    context = {'page': page, 'form': form}
    return render(request, 'users/user_form.html', context)


@login_required(login_url="login")
def updateAdmin(request, pk):
    if request.user.is_superuser:
        page = 'update'
        admin = Admin.objects.get(id=pk)
        usrn = admin.username
        form = CustomAdminCreationForm(instance=admin)
        

        if request.method == 'POST':

            if request.user.is_staff and request.user.is_superuser:
                form = CustomAdminCreationForm(request.POST, instance=admin)
                if form.is_valid():
                    admin = form.save(commit=False)
                    admin.prenom = admin.prenom.capitalize()
                    admin.nom = admin.nom.capitalize()
                    admin.cin = admin.cin.upper()
                    admin.username = admin.username.lower()
                    admin.email = admin.email.lower()
                    if usrn == admin.username:
                        admin.save()

                        messages.success(request, "L'administrateur a été mis à jour avec succès!")
                        return redirect('admins')
                    else:
                        try:
                            User.objects.get(username=admin.username)
                            messages.error(request, "Veuillez utiliser un autre nom d'utilisateur!")
                        except:
                            admin.save()

                            messages.success(request, "L'administrateur a été mis à jour avec succès!")
                            return redirect('admins')
                else:
                    messages.error(request, "Une erreur s'est produite lors de la modification de l'administrateur!")
            else:
                messages.error(request, "La modification des information des autres admins est refusée!!!")
    else:
        return redirect('admins')

    context = {'page': page, 'form': form}
    return render(request, 'users/user_form.html', context)


@login_required(login_url="login")
def deleteAdmin(request, pk):
    if request.user.is_superuser:
        admin = Admin.objects.get(id=pk)
        
        if request.method == 'POST':
            if admin.id == request.user.admin.id and request.user.is_staff and request.user.is_superuser:
                messages.error(request, "Opération refusée: Vous ne pouvez pas supprimer votre propre compte")

            elif admin.id != request.user.admin.id and request.user.is_staff and request.user.is_superuser:
                admin.delete()
                messages.success(request, "L'administrateur a été supprimé avec succès")
                return redirect('admins')
                
            else:
                messages.error(request, "Opération refusée: Vous ne pouvez pas supprimer les administrateurs!!!")
    else:
        return redirect('admins')
    
    context = {'object': admin}
    return render(request, 'users/delete.html', context)
    


@login_required(login_url = 'login')
def createStaff(request):
    if request.user.is_superuser:
        page = 'create'
        form = CustomStaffCreationForm()

        if request.method == 'POST':
            form = CustomStaffCreationForm(request.POST)
            if form.is_valid():
                staff = form.save(commit=False)
                staff.prenom = staff.prenom.capitalize()
                staff.nom = staff.nom.capitalize()
                staff.username = staff.username.lower()
                staff.email = staff.email.lower()
                staff.cin = staff.cin.upper()
                try:
                    User.objects.get(username=staff.username)
                    messages.error(request, "Veuillez utiliser un autre nom d'utilisateur!")
                except:
                    staff.save()

                    messages.success(request, "Le professionnel de santé a été créé avec succès!")
                    return redirect('staffs')

            else:
                messages.error(request, "Une erreur s'est produite lors de l'ajout du professionnel de santé!")
    else:
        return redirect('staffs')

    context = {'page': page, 'form': form}
    return render(request, 'users/user_form.html', context)


@login_required(login_url="login")
def updateStaff(request, pk):
    if request.user.is_superuser:
        page = 'update'
        professionel = Professional.objects.get(id=pk)
        usrn = professionel.username
        form = CustomStaffCreationForm(instance=professionel)

        if request.method == 'POST':
            
            form = CustomStaffCreationForm(request.POST, instance=professionel)
            if form.is_valid():
                staff = form.save(commit=False)
                staff.prenom = staff.prenom.capitalize()
                staff.nom = staff.nom.capitalize()
                staff.username = staff.username.lower()
                staff.email = staff.email.lower()
                staff.cin = staff.cin.upper()
                
                if usrn == staff.username:
                    staff.save()

                    messages.success(request, "Le professionnel de santé a été mis à jour avec succès!")
                    return redirect('staffs')
                else:
                    try:
                        User.objects.get(username=staff.username)
                        messages.error(request, "Veuillez utiliser un autre nom d'utilisateur!")
                    except:
                        staff.save()

                        messages.success(request, "Le professionnel de santé a été mis à jour avec succès!")
                        return redirect('staffs')

            else:
                messages.error(request, "Une erreur s'est produite lors de la modification du professionnel de santé!")
    else:
        return redirect('staffs')
    
    context = {'page': page, 'form': form}
    return render(request, 'users/user_form.html', context)


@login_required(login_url="login")
def deleteStaff(request, pk):
    if request.user.is_superuser:
        staff = Professional.objects.get(id=pk)
        
        if request.method == 'POST':
            staff.delete()
            messages.success(request, "Le professionnel de santé été supprimé!")
        
            return redirect('staffs')
    else:
        return redirect('staffs')
    
    context = {'object': staff}
    return render(request, 'users/delete.html', context)
  


@login_required(login_url = 'login')
def createPatient(request):
    page = 'create'
    form = CustomPatientCreationForm()

    if request.method == 'POST':
        form = CustomPatientCreationForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save(commit=False)
            if request.user.is_staff and request.user.is_superuser == False:
                patient.staff = request.user.professional
            patient.prenom = patient.prenom.capitalize()
            patient.nom = patient.nom.capitalize()
            patient.email = patient.email.lower()
            patient.location = patient.location.upper()
            patient.cin = patient.cin.upper()
            patient.save()

            filename = str(patient.filename)
            prediction = predictResult(filename)
            if prediction == 0:
                patient.result = True
            patient.save()

            messages.success(request, "Le patient a été ajouté avec succès!")
            return redirect('patient', pk=patient.id)
        
        else:
            messages.error(request, "Une erreur s'est produite lors de l'ajout du patient!")
            
    context = {'page': page, 'form': form}
    return render(request, 'users/user_form.html', context)


@login_required(login_url="login")
def updatePatient(request, pk):
    page = 'update'
    patient = Patient.objects.get(id=pk)
    form = CustomPatientCreationForm(instance=patient)
    sound = patient.soundfile

    if request.method == 'POST':
        
        form = CustomPatientCreationForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.prenom = patient.prenom.capitalize()
            patient.nom = patient.nom.capitalize()
            patient.email = patient.email.lower()
            patient.location = patient.location.upper()
            patient.cin = patient.cin.upper()
            patient.save()

            if patient.soundfile != sound:
                
                filename = str(patient.filename)

                prediction = predictResult(filename)
                if prediction == 0:
                    patient.result = True
                
                patient.is_sent = False
            patient.save()

            messages.success(request, "Les informations du patient ont été modifiées avec succès!")
            return redirect('patient', pk=patient.id)

        else:
            messages.error(request, "Une erreur s'est produite lors de la modification du patient!")

    context = {'page': page, 'form': form}
    return render(request, 'users/user_form.html', context)

  
@login_required(login_url="login")
def deletePatient(request, pk):
    patient = Patient.objects.get(id=pk)
    
    if request.method == 'POST':
        patient.delete()
        
        messages.success(request, "Le patient a été supprimé avec succès!")
        return redirect('patients')
    
    context = {'object': patient}
    return render(request, 'users/delete.html', context)


#inbox
#####################################################################

@login_required(login_url='login')
def inbox(request):
    usr = None
    messageRequests = None
    unreadCount = 0
    results = 3

    usr = request.user
    messageRequests = usr.messages.all()

    unreadCount = messageRequests.filter(is_read=False).count()
    
    custom_range, messageRequests = paginateObjects(request, messageRequests, results)

    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount, 'custom_range': custom_range}
    return render(request, 'users/inbox.html', context)



@login_required(login_url='login')
def viewMessage(request, pk):
    message = Message.objects.get(id=pk)
    profile = None

    if message.sender.is_superuser:
        profile = message.sender.admin
    else:
        profile = message.sender.professional

    if message.is_read == False:
        message.is_read = True
        message.save() 

    context = {'message': message, 'profile':profile}
    return render(request, 'users/message.html', context)


@login_required(login_url='login')
def createMessage(request, pk):
    recipient = None
    sender = None
    receiver = None
    try:
        if Admin.objects.get(id=pk):
            receiver = Admin.objects.get(id=pk)
            recipient = receiver.user
    except:
        if Professional.objects.get(id=pk):
            receiver = Professional.objects.get(id=pk)
            recipient = receiver.user

    try:
        sender = request.user
    except:
        sender = None

    form = MessageForm()
    if sender == recipient:
        return redirect('account')
    else:
        if request.method == 'POST':
            form = MessageForm(request.POST)

            if form.is_valid():
                message = form.save(commit=False)
                message.sender = sender
                message.recipient = recipient
                message.save()
                messages.success(request, "Votre message a été envoyé avec succès")
                return redirect('user-profile', pk=receiver.id)


    context = {"receiver": receiver, 'form': form}
    return render(request, 'users/message_form.html', context)



@login_required(login_url='login')
def contacts(request):
    if request.user.is_superuser:
        results = 3
        contactRequests = None
        unreadCount = 0
        
        contactRequests = Contact.objects.all()
    
        unreadCount = contactRequests.filter(is_read=False).count()

        custom_range, contactRequests = paginateObjects(request, contactRequests, results)
    else:
        return redirect('admins')

    context = {'contactRequests': contactRequests, 'unreadCount': unreadCount, 'custom_range': custom_range}
    return render(request, 'users/contacts.html', context)


@login_required(login_url='login')
def viewContact(request, pk):
    if request.user.is_superuser:
        contact = Contact.objects.get(id=pk)
        
        if contact.is_read == False:
            contact.is_read = True
            contact.save()
    else:
        return redirect('admins')        

    context = {'contact': contact}
    return render(request, 'users/contact.html', context)



@login_required(login_url='login')
def sendResult(request, pk):
    resultat = None
    patient = Patient.objects.get(id=pk)

    if request.method == 'POST':
        if patient.is_sent == False:
            patient.is_sent = True
            patient.save()

            host = "http://127.0.0.1:8000"
        
            subject = 'COPDiag - Votre Résultat 🩺'
            
            message = "Bienvenue, "+patient.prenom+".\n\n"

            if patient.result == True:
                message += "Votre résultat de prediction de la BPCO est: Positif\n"
                message += "Nous somme désolé d'apprendre que vous êtes malade.\n"
                message += "Nous vous souhaitons un bon rétablissement! Rétablis-toi vite!\n\n"
            elif patient.result == False:
                message += "Votre résultat de prediction de la BPCO est: Négatif\n"
                message += "Nous vous souhaitons une bonne santé.\n\n"

            message += "Coordialement,\n\n"
            message += "L'équipe COPDiag"

            email_sender = settings.EMAIL_HOST_USER
            send_mail(
                subject,
                message,
                email_sender,
                [patient.email],
                fail_silently=False,
            )
        
            messages.success(request, "Notification envoyée avec succès!")
            return redirect(request.GET['next'] if 'next' in request.GET else 'patients')
    
    context = {'object': patient}
    return render(request, 'users/send.html', context)
