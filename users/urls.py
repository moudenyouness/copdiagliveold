from django.urls import path
from . import views

urlpatterns = [
    
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    
    path('account/', views.userAccount, name="account"),
    path('edit-account/', views.editAccount, name="edit-account"),
    
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('', views.AdminsPage, name="admins"),
    path('create-admin/', views.createAdmin, name="create-admin"),
    path('update-admin/<str:pk>/', views.updateAdmin, name="update-admin"),
    path('delete-admin/<str:pk>/', views.deleteAdmin, name="delete-admin"),

    path('staffs/', views.StaffsPage, name="staffs"),
    path('create-staff/', views.createStaff, name="create-staff"),
    path('update-staff/<str:pk>/', views.updateStaff, name="update-staff"),
    path('delete-staff/<str:pk>/', views.deleteStaff, name="delete-staff"),

    path('patients/', views.PatientsPage, name="patients"),
    path('create-patient/', views.createPatient, name="create-patient"),
    path('patient/<str:pk>/', views.viewPatient, name="patient"),
    path('update-patient/<str:pk>/', views.updatePatient, name="update-patient"),
    path('delete-patient/<str:pk>/', views.deletePatient, name="delete-patient"),
    
    path('inbox/', views.inbox, name="inbox"),
    path('message/<str:pk>/', views.viewMessage, name="message"),
    path('create-message/<str:pk>', views.createMessage, name="create-message"),

    path('contacts/', views.contacts, name="contacts"),
    path('contact/<str:pk>/', views.viewContact, name="contact"),

    path('send-result/<str:pk>/', views.sendResult, name="send-result"),
    
]