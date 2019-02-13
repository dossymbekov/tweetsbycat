# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
import json
from .RetrieveTweets import main
from .GetTweetsByCategory import getTweetsByCategory

def index(request):
    return render(request, 'index.html', {})

def help(request):
    return render(request, 'help.html', {})

def policy(request):
    return render(request, 'policy.html', {})

def result(request):
    return render(request, 'result.html', {})

classdict1 = {    1: "Animals",
                 2: "Agriculture",
                 3: "Architecture",
                 4: "Art and Photography",
                 5: "Automobile",
                 6: "Business & Finance",
                 7: "Children",
                 8: "Comics & Humor",
                 9: "Computers and Electronics",
                 10: "Food and Beverages",
                 11: "Education",
                 12: "Ethnic",
                 13: "Fashion and Style",
                 14: "Health and Fitness",
                 15: "History",
                 16: "Literature",
                 17: "Medical",
                 18: "Music",
                 19: "Politics",
                 20: "Psychology",
                 21: "Religion",
                 22: "Science and Nature",
                 23: "Sports and Recreation",
                 24: "TV and Movie",
                 25: "Weather"}

classdict2 = {   "Animals": 1,
                 "Agriculture": 2,
                 "Architecture": 3,
                 "Art and Photography": 4,
                 "Automobile": 5,
                 "Business & Finance": 6,
                 "Children": 7,
                 "Comics & Humor": 8,
                 "Computers and Electronics": 9,
                 "Food and Beverages": 10,
                 "Education": 11,
                 "Ethnic": 12,
                 "Fashion and Style": 13,
                 "Health and Fitness": 14,
                 "History": 15,
                 "Literature": 16,
                 "Medical": 17,
                 "Music": 18,
                 "Politics": 19,
                 "Psychology": 20,
                 "Religion": 21,
                 "Science and Nature": 22,
                 "Sports and Recreation": 23,
                 "TV and Movie": 24,
                 "Weather": 25}

@api_view(['GET', 'POST'])
def getTweets(request):
    
    if request.method == 'POST':
        topic = request.data.get('data') 
        #get topic from front-end
    #topic = request.data.get('data') 
    cat_name = request.data['name']
  
    tweets_list = getTweetsByCategory(str(classdict2[cat_name]))
    #tweets=['111111','2222222222','33333333333']
    return HttpResponse(json.dumps({'tweets':tweets_list}))

def getTopics(request):
    city = request.GET['city']
    dictt = main(city)
    keys_list = list(dictt.keys())
    pie_series2 = { 
        'data': [
                  [classdict1[keys_list[0]],  dictt[keys_list[0]]],
                  [classdict1[keys_list[1]],  dictt[keys_list[1]]],
                  [classdict1[keys_list[2]],  dictt[keys_list[2]]],
                  [classdict1[keys_list[3]],  dictt[keys_list[3]]],
                  [classdict1[keys_list[4]],  dictt[keys_list[4]]]
                ]
    }
    '''
    pie_series1 = { 
        #put the first 5 categories & their percentage by descending sort
        'data': [
			['Animals & Pets',   45.0],
			['Antiques & Collectibles',  26.8],
			['Architecture',12.8],
			['Art & Photography ',    8.5],
			['Auto & Cycles',     6.1]
		]
    }
    '''
    series = json.dumps(pie_series2, separators=(',', ':')) 
    return render(request, 'result.html', {'series': series})