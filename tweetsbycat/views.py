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
                 
states_data = { "32.361538,-86.279118":"Alabama", 
                "58.301935,-134.419740":"Alaska",
                "33.448457,-112.073844":"Arizona",
                "34.736009,-92.331122":"Arkansas",
                "38.555605,-121.468926":"California",
                "39.7391667,-104.984167":"Colorado",
                "41.767,-72.677":"Connecticut",
                "39.161921,-75.526755":"Delaware",
                "30.4518,-84.27277":"Florida",
                "33.76,-84.39":"Georgia",
                "21.30895,-157.826182":"Hawaii",
                "43.613739,-116.237651":"Idaho",
                "39.783250,-89.650373":"Illinois",
                "39.790942,-86.147685":"Indiana",
                "41.590939,-93.620866":"Iowa",
                "39.04,-95.69":"Kansas",
                "38.197274,-84.86311":"Kentucky",
                "30.45809,-91.140229":"Louisiana",
                "44.323535,-69.765261":"Maine",
                "38.972945,-76.501157":"Maryland",
                "42.2352,-71.0275":"Massachusetts",
                "42.7335,-84.5467":"Michigan",
                "44.95,-93.094":"Minnesota",
                "32.320,-90.207":"Mississippi",
                "38.572954,-92.189283":"Missouri",
                "46.595805,-112.027031":"Montana",
                "40.809868,-96.675345":"Nebraska",
                "39.160949,-119.753877":"Nevada",
                "43.220093,-71.549127":"New Hampshire",
                "40.221741,-74.756138":"New Jersey",
                "35.667231,-105.964575":"New Mexico",
                "42.659829,-73.781339":"New York",
                "35.771,-78.638":"North Carolina",
                "48.813343,-100.779004":"North Dakota",
                "39.962245,-83.000647":"Ohio",
                "35.482309,-97.534994":"Oklahoma",
                "44.931109,-123.029159":"Oregon",
                "40.269789,-76.875613":"Pennsylvania",
                "41.82355,-71.422132":"Rhode Island",
                "34.000,-81.035":"South Carolina",
                "44.367966,-100.336378":"South Dakota",
                "36.165,-86.784":"Tennessee",
                "30.266667,-97.75":"Texas",
                "40.7547,-111.892622":"Utah",
                "44.26639,-72.57194":"Vermont",
                "37.54,-77.46":"Virginia",
                "47.042418,-122.893077":"Washington",
                "38.349497,-81.633294":"West Virginia",
                "43.074722,-89.384444":"Wisconsin",
                "41.145548,-104.802042":"Wyoming" }

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
    statename = states_data[city]
    pie_series2 = { 
        'data': [
                  [classdict1[keys_list[0]],  dictt[keys_list[0]]],
                  [classdict1[keys_list[1]],  dictt[keys_list[1]]],
                  [classdict1[keys_list[2]],  dictt[keys_list[2]]],
                  [classdict1[keys_list[3]],  dictt[keys_list[3]]],
                  [classdict1[keys_list[4]],  dictt[keys_list[4]]]
                ], 'city': [statename]
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
