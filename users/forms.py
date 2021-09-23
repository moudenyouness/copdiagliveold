from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from .models import Message , Patient , Professional , Admin 

class CustomAdminCreationForm(ModelForm):#UserCreationForm
    class Meta:
        model =  Admin 
        fields = ['prenom','nom','username','cin','email']
        labels = {
            'prenom':'Prenom:',
            'nom':'Nom:',
            "username":"Nom d'utilisateur:",
            'cin':'CIN:',
            'email':'Email:',
        }
        # exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(CustomAdminCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input form-control'})


class CustomStaffCreationForm(ModelForm):
    class Meta:
        model = Professional
        fields = '__all__'
        labels = {
            'prenom':'Prenom:',
            'nom':'Nom:',
            "username":"Nom d'utilisateur:",
            'cin':'CIN:',
            'email':'Email:',
            'location':'Ville:',
            'age':'Age:',
            'gender':'Genre: ',
            'phone':'Telephone:',
        }
        exclude = ['user']
        

    def __init__(self, *args, **kwargs):
        super(CustomStaffCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input form-control'})
        GENDER_CHOICES = (
            ('homme','Homme'),
            ('femme','Femme'),
        )
        self.fields['gender'] = forms.ChoiceField(label='Genre', widget=forms.RadioSelect, choices=GENDER_CHOICES)


class CustomPatientCreationForm(ModelForm, forms.Form):
    class Meta:
        model = Patient
        fields = '__all__'
        labels = {
            'prenom':'Prenom:',
            'nom':'Nom:',
            'cin':'CIN:',
            'email':'Email:',
            'location':'Ville:',
            'age':'Age:',
            'gender':'Genre: ',
            'phone':'Telephone:',
            'soundfile':'Ficher Audio:',
        }
        exclude = ['is_sent', 'result', 'staff']
        

    def __init__(self, *args, **kwargs):
        super(CustomPatientCreationForm, self).__init__(*args, **kwargs)

        # for name, field in self.fields.items():
        #     field.widget.attrs.update({'class':'input form-control'})
        
        self.fields['prenom'].widget.attrs.update(
            {'class':'input form-control'})
        self.fields['nom'].widget.attrs.update(
            {'class':'input form-control'})
        self.fields['cin'].widget.attrs.update(
            {'class':'input form-control'})
        self.fields['email'].widget.attrs.update(
            {'class':'input form-control'})
        self.fields['location'].widget.attrs.update(
            {'class':'input form-control'})
        self.fields['age'].widget.attrs.update(
            {'class':'input form-control', 'style':'max-width:150px;','max':'130', 'min':'1'})

        # self.fields['gender'].widget.attrs.update(
        #     {'class':'input form-control', 'style':'max-width:150px;'})
        GENDER_CHOICES = (
            ('homme','Homme'),
            ('femme','Femme'),
        )
        self.fields['gender'] = forms.ChoiceField(label='Genre', widget=forms.RadioSelect, choices=GENDER_CHOICES)
        

        self.fields['phone'].widget.attrs.update(
            {'class':'input form-control'})

        self.fields['soundfile'].widget.attrs.update(
            {'class':'input form-control form-control-lg', 'accept':'audio/*'}) #

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']
        
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
    
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input form-control'})