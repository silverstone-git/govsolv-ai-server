from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

# Create your views here.

def index(request):
    return HttpResponse("Hemlo domst")

@csrf_exempt
def spam(request):
    access = ""
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        access = body['access']
    except Exception as error:
        print(error)
    if access and access == settings.ACCESS_TOKEN:
        return HttpResponse("{spam:true, probability:70}")
    else:
        return HttpResponse("404")