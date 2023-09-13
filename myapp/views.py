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
from model_handler import predict_dept

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
    except Exception as error:
        print(error)

    if access == settings.ACCESS_TOKEN:
        return JsonResponse({'success': False, 'data': {}, 'message': 'Wrong Access Token'}, status = 404)

    model_error = False
    spam_model = True


    department = False
    if not spam:
        try:
            department = predict_dept(message)
            if department == -1:
                model_error = True
        except:
            pass

    #####
    # data -> {"spam"; "dept", ""}
    #####
    
    if access and message and not model_error and department:
        return JsonResponse({'success': True, 'data': {'spam': spam_res, 'department': department}, 'message': 'Successfully evaluated'}, status = 200)
    elif access and message and not department:
        return JsonResponse({'success': False, 'data': {}, 'message': 'Department Decision error'}, status = 500)

    elif model_error:
        return JsonResponse({'success': False, 'data': {}, 'message': 'Model File Parsing Error'}, status = 500)

    else:
        return JsonResponse({'success': False, 'data': {}, 'message': 'Missing some properties in request, did you give message and access in the request body?'}, status = 400)
