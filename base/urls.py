from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('informations/', views.infos, name="infos"),
    path('statistiques/', views.stats, name="stats"),
    path('result/', views.result, name="result"),
    path('contact/', views.contact, name="contact"),

]