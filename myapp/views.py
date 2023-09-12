from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from tf.keras.preprocessing.text import Tokenizer
from tf.keras.preprocessing.sequence import pad_sequences
import json
import pickle
from random import random

# Create your views here.

def index(request):
    return HttpResponse("Hemlo domst")


def spam_check(message, spam_model):
    # take in a message, check spam, send Boolean and Integer in a list
    # denoting the tolerance checked value for if message is indeed spam or not
    # and the integer stands for the probability in percentage
    probability = int(random() * 100)
    probRand = random()
    isSpam = True
    if probRand > 0.5:
        isSpam = False


    max_len = 50
    trunc_type = "post"
    padding_type = "post"
    oov_tok = "<OOV>"
    vocab_size = 500
    
    tokenizer = Tokenizer(num_words = vocab_size, char_level=False, oov_token = oov_tok)

    
    def predict_spam(predict_msg):
        new_seq = tokenizer.texts_to_sequences(predict_msg)
        padded = pad_sequences(new_seq, maxlen =max_len,
        padding = padding_type,
        truncating=trunc_type)
        return (spam_model.predict(padded))

    a=predict_spam(message)
    last_prob = a[-1]

    return isSpam



"""
def which_dept(message):
    # string ->  preprocessing -> model -> class -> department string
    return "Department ??"
"""

"""
def spam_check(message):
    if random() > 0.5:
        return True
    else:
        return False
"""




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

    spam_model = False
    model_error = False
    with open("spam_model.pkl", 'rb') as spam_model_file:
        try:
            spam_model = pickle.load(spam_model_file)
        except Exception as e:
            print(e)
            model_error = True

    # process the spam model

    spam_res = [True, 100]
    if spam_model:
        spam_res = [spam_check(message, spam_model), 100]
        spam_probability = spam_res[1]
    else:
        model_error = True


    

    #####
    # data -> {"spam"; "dept", ""}
    #####
    
    if access and message and access == settings.ACCESS_TOKEN and not model_error:
        return JsonResponse({'success': True, 'data': {'spam': spam_res[0], 'probability': spam_res[1]}, 'message': 'Successfully evaluated'}, status = 200)
    elif access != settings.ACCESS_TOKEN and not model_error:
        return JsonResponse({'success': False, 'data': {}, 'message': 'Wrong Access Token'}, status = 404)
    elif model_error:
        return JsonResponse({'success': False, 'data': {}, 'message': 'Model File Parsing Error'}, status = 400)

    else:
        return JsonResponse({'success': False, 'data': {}, 'message': 'Missing some properties in request, did you give message and access in the request body?'}, status = 400)
