# -*- coding: utf-8 -*-
from django.shortcuts import render

def index(request):
    return render(request, 'index.html', {})

def help(request):
    return render(request, 'help.html', {})

def policy(request):
    return render(request, 'policy.html', {})

def result(request):
    return render(request, 'result.html', {})