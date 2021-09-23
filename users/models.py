from django.db import models
from django.contrib.auth.models import User
import os
import uuid

# Create your models here.


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    prenom = models.CharField(max_length=200, blank=True, null=True)
    nom = models.CharField(max_length=200, blank=True, null=True)
    cin = models.CharField(max_length=8, blank=False, null=False, unique=True)
    username = models.CharField(max_length=200, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.prenom+" "+self.nom)

    class Meta:
        ordering = ['created']


class Professional(models.Model):
    GENDER_TYPE = (
        ('homme','Homme'),
        ('femme','Femme'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nom = models.CharField(max_length=200, blank=True, null=True)
    prenom = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    cin = models.CharField(max_length=8, blank=False, null=False, unique=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=200, choices=GENDER_TYPE) #2 choices: homme ou femme
    phone = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.prenom+" "+self.nom)

    class Meta:
        ordering = ['created']


class Patient(models.Model):
    GENDER_TYPE = (
        ('homme','Homme'),
        ('femme','Femme'),
    )
    staff = models.ForeignKey(Professional, null=True, blank=True, on_delete=models.SET_NULL)
    prenom = models.CharField(max_length=200, blank=False, null=False)
    nom = models.CharField(max_length=200, blank=False, null=False)
    cin = models.CharField(max_length=8, blank=False, null=False, unique=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=200, choices=GENDER_TYPE) #2 choices: homme ou femme
    phone = models.CharField(max_length=200, blank=True, null=True)
    soundfile = models.FileField(null=True, blank=True)#, upload_to='soundfiles/'
    result = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.prenom+" "+self.nom)

    @property
    def filename(self):
        return os.path.basename(self.soundfile.name)

    class Meta:
        ordering = ['is_sent','created']
    
    @property
    def soundURL(self):
        try:
            url = self.soundfile.url
        except:
            url = "" 
        return url


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']


# class Notification(models.Model):
#     patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
#     is_sent = models.BooleanField(default=False, null=True)
#     id = models.UUIDField(default=uuid.uuid4, unique=True,
#                           primary_key=True, editable=False)
