from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from random import random

# Create your views here.

def index(request):
    return HttpResponse("Hemlo domst")


def spam_check(message):
    # take in a message, check spam, send Boolean and Integer in a list
    # denoting the tolerance checked value for if message is indeed spam or not
    # and the integer stands for the probability in percentage
    probability = int(random() * 100)
    probRand = random()
    isSpam = True
    if probRand > 0.5:
        isSpam = False
    return [isSpam, probability]


@csrf_exempt
def spam(request):
    access = ""
    message = ""
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        access = body['access']
        message = body['message']
    except Exception as error:
        print(error)
    spam_res = spam_check(message)
    spam_string = "true"
    if spam_res[0]:
        spam_string = "true"
    else:
        spam_string = "false"
    spam_probability = str(spam_res[1])
    if access and message and access == settings.ACCESS_TOKEN:
        return HttpResponse("{'success': true, 'data': {spam: " + spam_string + ", probability: " + spam_probability + "}, 'message': 'Successfully evaluated'}", status = 200)
    elif access != settings.ACCESS_TOKEN:
        return HttpResponse("{'success': false, 'data': {}, 'message': 'Wrong Access Token'}", status = 404)
    else:
        return HttpResponse("{'success': false, 'data': {}, 'message': 'Missing some properties in request, did you give message and access in the request body?'}", status = 400)