import os
from django.db.models import Q
from .models import Patient
from base.models import Contact
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings

import sklearn
import xgboost as xgb
import pandas as pd
import pickle
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages


clf_xg = xgb.XGBClassifier(n_estimators=100) 
ROOT = settings.MEDIA_ROOT
DIR = settings.MEDIA_URL
BASE_DIR = settings.BASE_DIR

r = robjects.r
r('''keeps <- c("meanfreq","sd","median","Q25", "Q75","IQR","skew","kurt","sp.ent","sfm","mode", "centroid","meanfun","minfun","maxfun","meandom","mindom","maxdom","dfrange", "modindx")
    library(tuneR)
    library(seewave)
    library(warbleR)
    ''')

def predictResult(filename):
    result = 0
    model = None
    
    os.chdir(ROOT)
    
    robjects.globalenv['fileName'] = filename
    r('''
        data <- data.frame()
        data <- data.frame(fileName, 0, 0, 20)
        names(data) <- c('sound.files', 'selec', 'start', 'end')
        a <- specan(X=data , bp = c(0,22), wl = 2048, threshold = 5, parallel = 1)
        acoustics = a[keeps]
        ''')
    acoustics = robjects.r.acoustics

    meanfreq = (acoustics[0])[0]
    sd = (acoustics[1])[0]
    median = (acoustics[2])[0]
    Q25 = (acoustics[3])[0]
    Q75 = (acoustics[4])[0]
    IQR = (acoustics[5])[0]
    skew = (acoustics[6])[0]
    kurt = (acoustics[7])[0]
    sp_ent = (acoustics[8])[0]
    sfm = (acoustics[9])[0]
    mode = (acoustics[10])[0]
    centroid = (acoustics[11])[0]
    meanfun = (acoustics[12])[0]
    minfun = (acoustics[13])[0]
    maxfun = (acoustics[14])[0]
    meandom = (acoustics[15])[0]
    mindom = (acoustics[16])[0]
    maxdom = (acoustics[17])[0]
    dfrange = (acoustics[18])[0]
    modindx = (acoustics[19])[0]

    os.chdir(BASE_DIR)
    
    f = open('rf_model.sav','rb')
    model = pickle.load(f)
    f.close()

    x = [[meanfreq, sd, median, Q25, Q75, IQR, skew, kurt, sp_ent, sfm, mode,
    centroid, meanfun, minfun, maxfun, meandom, mindom, maxdom, dfrange, modindx]]

    result = int(model.predict(x))

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