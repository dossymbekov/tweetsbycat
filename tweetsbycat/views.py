# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
import json

def index(request):
    return render(request, 'index.html', {})

def help(request):
    return render(request, 'help.html', {})

def policy(request):
    return render(request, 'policy.html', {})

def result(request):
    return render(request, 'result.html', {})

@api_view(['GET', 'POST'])
def getTweets(request):
    if request.method == 'POST':
        topic = request.data.get('data') 
        #get topic from front-end
    tweets=['111111','2222222222','33333333333']
    return HttpResponse(json.dumps({'tweets':tweets}))


def getTopics(request):
    city = request.GET['city']
    #put the function which extract and prepocess the data here
    pie_series1 = { 
        #put the first 5 categories & their percentage by descending sort
        'data': [
			['Animals & Pets',   45.0],
			['Antiques & Collectibles',       26.8],
			['Architecture',12.8],
			['Art & Photography ',    8.5],
			['Auto & Cycles',     6.1],
			['Others',   0.8]
		]
    }
    series = json.dumps(pie_series1, separators=(',', ':')) 
    return render(request, 'result.html', {'series': series})

    