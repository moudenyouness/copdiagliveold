from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from users.models import Patient
from .forms import ContactForm


# Create your views here.
##############################################################################################################
def home(request):
    
    context = {}
    return render(request, 'base/index.html', context)

def infos(request):
    
    context = {}
    return render(request, 'base/informations.html', context)
    
def stats(request):
    
    context = {}
    return render(request, 'base/statistiques.html', context)

def result(request):
    cin = ''
    patient = None
    resultat = None

    if request.GET.get('cin'):
        cin = request.GET.get('cin')
        try:
            patient = Patient.objects.get(cin=cin)
            resultat = patient.result

            if resultat:
                resultat = 'Positive'
            else:
                resultat = 'Negative'
        except:
            messages.error(request, 'CIN invalide')
    
    
    context = {'resultat': resultat, 'patient': patient, 'cin': cin}
    return render(request, 'base/result.html', context)


def contact(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            contact = form.save(commit=False)
            contact.name = contact.name.capitalize()
            contact.email = contact.email.lower()
            
            contact.save()
            messages.success(request, 'Your message was successfully sent')
            return redirect('contact')
        else:
            messages.error(request, 'Message could not be sent')


    context = {'form': form}
    return render(request, 'base/contact_form.html', context)
#############################################################################################################
