from django import template
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

register = template.Library()

from ..models import Message
from base.models import Contact

#  @login_required(login_url = 'login')
# @register.inclusion_tag('users/administrateur/topbar.html')
@register.simple_tag
def total_messages(profile):
    
    messageR = profile.messages.all()
    count = messageR.filter(is_read=False).count()

    return count



@register.simple_tag
def total_contacts():
    
    contactR = Contact.objects.all()
    contactCount = contactR.filter(is_read=False).count()

    return contactCount

