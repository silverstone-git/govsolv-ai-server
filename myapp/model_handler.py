import pickle
import pandas as pd
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

REPLACE_BY_SPACE_RE = re.compile('[/(){}\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')

def clean_text(text):
    
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text. substitute the matched string in REPLACE_BY_SPACE_RE with space.
    text = BAD_SYMBOLS_RE.sub('', text) # remove symbols which are in BAD_SYMBOLS_RE from text. substitute the matched string in BAD_SYMBOLS_RE with nothing. 
    text = text.replace('x', '')
    #text = ' '.join(word for word in text.split() if word not in STOPWORDS) # remove stopwors from text
    return text

# The maximum number of words to be used. (most frequent)
MAX_NB_WORDS = 100
# Max number of words in each complaint.
MAX_SEQUENCE_LENGTH = 20
# This is fixed.
EMBEDDING_DIM = 2

#1:  "Dept of Jal Shakti"
#Test Case:
# 0: These toll rate problems have become a major headache. I'm pleading for someone to step in and bring some order to this chaos. Personally, it's been a constant headache dealing with these issues.
#1: "I'm concerned about the water quality in our homes. It's been consistently dirty, and we're worried about its impact on our health."

def predict_dept(message):

    model = False
    with open("department_model.pkl", "rb") as f1:
        model = pickle.load(f1)

    if not model:
        return -1

    DF=pd.DataFrame({'message':[message]})
    DF['message']=DF['message'].apply(clean_text)
    
    tokenizer = Tokenizer(num_words=MAX_NB_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
    tokenizer.fit_on_texts(DF['message'].values)
    
    x=tokenizer.texts_to_sequences(DF['message'].values)
    x = pad_sequences(x, maxlen=MAX_SEQUENCE_LENGTH)
    y=model.predict(x)

    ans=int(y[0][0]>=0.6)
    return ans


def predict_spam(message):

    model = False
    with open("spam_model.pkl", "rb") as f1:
        model = pickle.load(f1)

    if not model:
        return -1

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
        return (model.predict(padded))

    a=predict_spam(message)
    last_prob = a[-1]

    isSpam = True
    if last_prob < 0.1:
        isSpam = False

    return isSpam




if __name__ == "__main__":
    msg = input("Enter grievance: ")
    spam = predict_spam(msg)
    print("spam was: ", spam)
    if not spam:
        department = predict_dept(msg)
        print("department was: ", department)
