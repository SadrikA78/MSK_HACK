#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.admin.models import LogEntry
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import datetime
from django.core.serializers import serialize
from .forms import *
from django.contrib.auth.models import User

from plotly.offline import plot
import pandas as pd
import plotly.graph_objects as go
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, roc_auc_score
import xlrd
import time
import telebot
from telebot import types
from absl import logging

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps
from scipy.spatial import cKDTree
from skimage.feature import plot_matches
from skimage.measure import ransac
from skimage.transform import AffineTransform
from six import BytesIO

import tensorflow as tf

import tensorflow_hub as hub
from six.moves.urllib.request import urlopen
import urllib.request
import skimage

import os
import json
from datetime import datetime
import time
import csv
import codecs
import glob
from itertools import accumulate
from os import walk


def yandex_coor(adress):
    client = Client("your-api-key")
    coordinates = client.coordinates(adress)
    return coordinates

def run_delf(image):
  np_image = np.array(image)
  float_image = tf.image.convert_image_dtype(np_image, tf.float32)

  return delf(
      image=float_image,
      score_threshold=tf.constant(100.0),
      image_scales=tf.constant([0.25, 0.3536, 0.5, 0.7071, 1.0, 1.4142, 2.0]),
      max_feature_num=tf.constant(1000))
def match_images(data, result2):
    distance_threshold = 0.6

    num_features_1 = len(data['locations'])
    num_features_2 = result2['locations'].shape[0]

    d1_tree = cKDTree(data['descriptors'])
    _, indices = d1_tree.query(
        result2['descriptors'],
        distance_upper_bound=distance_threshold)

    locations_2_to_use = np.array([
        result2['locations'][i,]
        for i in range(num_features_2)
        if indices[i] != num_features_1
    ])
    locations_1_to_use = np.array([
        data['locations'][indices[i]]
        for i in range(num_features_2)
        if indices[i] != num_features_1
    ])

    _, inliers = ransac(
        (locations_1_to_use, locations_2_to_use),
        AffineTransform,
        min_samples=3,
        residual_threshold=20,
        max_trials=1000)
    return {"inliers": sum(inliers)}
    
    
    
def prognoz(path_im_test, name_test, list_f, destfolder, result_path):
    delf = hub.load('model').signatures['default']
    result1 = run_delf(Image.open(path_im_test+name_test))
    inliers_counts = {}
    inliers_counts['name'] = name_test
    inliers_rez = []
    for i in list_f:
        j = i.split('.json')[0]
        with open(destfolder+i, 'r') as fp:
            data = json.load(fp)
        try:
            result = match_images(data, result1)
            inliers_rez.append({"index": j, "inliers": int(result['inliers'])})
        except:
            pass
    top_match = sorted(inliers_rez, key=lambda k: k['inliers'], reverse=True)[0]
    inliers_counts['index'] = top_match['index']
    inliers_counts['inliers'] = top_match['inliers']
    with open(result_path+name_test.split('.jpg')[0]+'.json', 'w') as fp:
        json.dump(inliers_counts, fp)

def registration(request):
    if request.POST:
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
        return HttpResponseRedirect('/accounts/login/')
    content = {}
    return render(request, 'registration/registration.html', content)   
@login_required
def index(request):
    types = Type.objects.all()
    content = {'types':types}   
    return render(request, 'log_pay/index.html', content)
@login_required
def mission(request):
    types = Type.objects.all()
    if 'new_type' in request.POST:
        new_type = Type(name=request.POST['name'], example = request.POST['input_file_type'])
        new_type.save()
        return HttpResponseRedirect('/')
    content = {'types':types}            
    return render(request, 'log_pay/missions.html', content)  

@login_required
def types(request, types_id):
    df = pd.read_excel('11.xlsx')
    types = Type.objects.all()
    type1 = Type.objects.get(id=types_id)
    
    df=(df.loc[df['Тип документа'] == type1.name])
    names = df.values.tolist() 
    
    fig_al =  go.Figure()
    scatter = go.Densitymapbox(lat=df['широта '], lon=df['долгота'], z=df['Дата'],
                                 radius=10)
    fig_al.add_trace(scatter)
    
    fig_al.update_layout(
        autosize=True,
        width=1000,
        height=700,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=2
        ),
        mapbox_style="stamen-terrain",
        mapbox_center_lon=57,
        mapbox_center_lat=30
    )

    fig_al.update_yaxes(automargin=True)
    plt_div_al = plot(fig_al, output_type='div', include_plotlyjs = True)
    
    content = {'types':types, 'type':type1, 'names':names, 'plt_div_al':plt_div_al}            
    return render(request, 'log_pay/types.html', content)  
@login_required
def history(request):
    content = {}            
    return render(request, 'log_pay/history.html', content)  
def one(request):
    types = Type.objects.all()
    mapbox_access_token = ""
    fig = go.Figure(go.Scattermapbox(
            lat=['55.601996'],
            lon=['37.622614'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=19
            ),
            text=["н.д."],
        ))

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=dict(
                lat=55.6,
                lon=37.6
            ),
            pitch=0,
            zoom=7
        ),
        width=1200, height=600
    )
    fig.update_yaxes(automargin=True)
    plt_fig = plot(fig, output_type='div', include_plotlyjs = True)
    content = {'plt_fig':plt_fig, 'types':types}   
    return render(request, 'log_pay/one.html', content)  

 #Add URL page
@login_required
def add_source(request):
    if request.POST:
        if 'http' in str(request.POST['url']):
            URL(url=request.POST['url']).save()
        if 'http' in str(request.POST['url2']):
            URL(url=request.POST['url2']).save()
        if 'http' in str(request.POST['url3']):
            URL(url=request.POST['url3']).save()
        if 'http' in str(request.POST['url4']):
            URL(url=request.POST['url4']).save()
        if 'html' in str(request.POST['input_file']):
            HTML(name=str(request.POST['input_file']), file=request.POST['input_file']).save()
        return HttpResponseRedirect('/mission/')
    content = {}
    return render(request, 'log_pay/add_source.html', content) 
    