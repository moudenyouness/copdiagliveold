import os
from django.db.models import Q
from .models import Patient
from base.models import Contact
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings

import sklearn
#import xgboost as xgb
import pandas as pd
import pickle
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages


#clf_xg = xgb.XGBClassifier(n_estimators=100) 
ROOT = settings.MEDIA_ROOT
DIR = settings.MEDIA_URL
BASE_DIR = settings.BASE_DIR


def predictResult(filename):
    result = 0
    return int(result)



def paginateObjects(request, Obj, results):
    
    page = request.GET.get('page')
    paginator = Paginator(Obj, results)

    try:
        Obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        Obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        Obj = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)


    return custom_range, Obj

# def searchPatients(request):
#     search_query = ''

#     if request.GET.get('search_query'):
#         search_query = request.GET.get('search_query')

#     patients = Patient.objects.distinct().filter(
#         Q(prenom__icontains=search_query) | 
#         Q(nom__icontains=search_query) | 
#         Q(cin__icontains=search_query) | 
#         Q(email__icontains=search_query) | 
#         Q(age__icontains=search_query) | 
#         Q(phone__icontains=search_query) | 
#         Q(gender__icontains=search_query) | 
#         Q(location__icontains=search_query) | 
#         Q(staff__nom__icontains=search_query) | 
#         Q(staff__prenom__icontains=search_query) |
#         )

#     return patients, search_query
