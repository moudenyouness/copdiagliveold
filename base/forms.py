from django.forms import ModelForm
from .models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'body']
        
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
    
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control border border-primary bg-white text-primary'})

