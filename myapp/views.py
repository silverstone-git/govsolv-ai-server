from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from random import random
import pandas as pd
from .model_handler import *

# Create your views here.


def index(request):
    return render(request, "model_check.html", {"access_token": settings.ACCESS_TOKEN.strip()})


@csrf_exempt
def evaluate_message(request):
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

    print("\n MESSAGE RECEIVED -> {}  \n".format(message))

    # call spam
    spam = predict_spam(message)

    if spam == -1:
        model_error = True

    print("\nspam from handler is: \n", spam)

    department = -1
    if spam != -1 and not spam:

        print("\n trying getting the department\n")
        try:
            department = predict_dept(message)
            print("department -> ", department)
            if department == -1:
                print("dept model handler gave error, setting response 500")
                model_error = True
        except:
            print("\n smoe eror occured while trying yhe predict_dept function\n")
            pass

    if model_error:
        return JsonResponse({'success': False, 'data': {}, 'message': 'Model File Parsing Error'}, status = 500)
    elif access and message:
        return JsonResponse({'success': True, 'data': {'spam': spam, 'department': int(department)}, 'message': 'Successfully evaluated'})
    else:
        return JsonResponse({'success': False, 'data': {}, 'message': 'Missing some properties in request, did you give message and access in the request body?'}, status = 400)
