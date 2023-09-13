from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json
import pickle
from random import random
import pandas as pd
import re
from .model_handler import *

# Create your views here.


def index(request):
    return HttpResponse("Hemlo domst")


@csrf_exempt
def evaulate_message(request):
    access = ""
    message = ""
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        access = body['access']

        message = body['message']
        print("body access: ", access)
    except Exception as error:
        print(error)


    if access.strip() != settings.ACCESS_TOKEN.strip():
        return JsonResponse({'success': False, 'data': {}, 'message': 'Wrong Access Token'}, status = 404)

    model_error = False
    spam_model = True

    # call spam
    spam = predict_spam(message)

    if spam == -1:
        model_error = True

    print("\nspam from handler is: \n", spam)

    department = -1
    if spam != -1 and not spam:
        try:
            department = predict_dept(message)
            print("department -> ", department)
            if department == -1:
                model_error = True
        except:
            pass

    if access and message and not model_error:
        return JsonResponse({'success': True, 'data': {'spam': spam, 'department': department}, 'message': 'Successfully evaluated'}, status = 200)
    elif access and message and department == -1:
        return JsonResponse({'success': False, 'data': {}, 'message': 'Department Decision error'}, status = 500)

    elif model_error:
        return JsonResponse({'success': False, 'data': {}, 'message': 'Model File Parsing Error'}, status = 500)

    else:
        return JsonResponse({'success': False, 'data': {}, 'message': 'Missing some properties in request, did you give message and access in the request body?'}, status = 400)
