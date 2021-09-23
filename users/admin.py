from django.contrib import admin

# Register your models here.
from .models import Professional , Message , Patient , Admin  #, Notification 


admin.site.register(Patient)
admin.site.register(Professional)
admin.site.register(Admin)
admin.site.register(Message)
# admin.site.register(Notification)