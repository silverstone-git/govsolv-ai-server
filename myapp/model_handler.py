import pickle
import pandas as pd
import re
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

import pathlib
parent_dir = pathlib.Path(__file__).parent.resolve()

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


def get_train_messages():
    train_msg = -1

    df = -1
    with open(parent_dir / "train_msg.pkl", "rb") as f1:
        #train_msg = pickle.load(f1)
        df = pd.compat.pickle_compat.load(f1)
    return df



def predict_dept(message):

    model = False
    with open(parent_dir / "department_model.pkl", "rb") as f1:
        model = pickle.load(f1)

    """
    training_messages = get_train_messages()
    if training_messages == -1:
        # file error in train msg case
        return -1
    """

    if not model:
        print("\n there is no such thing \n")
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
    with open(parent_dir / "spam_model.pkl", "rb") as f1:
        model = pickle.load(f1)

    training_messages = get_train_messages()

    """
    if training_messages == -1:
        # file error in train msg case
        return -1
    """

    if not model:
        return -1

    max_len = 50
    trunc_type = "post"
    padding_type = "post"
    oov_tok = "<OOV>"
    vocab_size = 500
    
    tokenizer = Tokenizer(num_words = vocab_size, char_level=False, oov_token = oov_tok)

    
    def predict_spam_inner(predict_msg):
        df = pd.DataFrame({"message": [predict_msg]})

        print("df of the train messages: ", training_messages)
        tokenizer.fit_on_texts(training_messages)
        new_seq = tokenizer.texts_to_sequences(df['message'].values)
        padded = pad_sequences(new_seq, maxlen =max_len,
        padding = padding_type,
        truncating=trunc_type)
        return (model.predict(padded))

    a=predict_spam_inner(message)
    last_prob = a[0][-1]

    print("in the end, the last_prob is: ", last_prob)

    isSpam = True
    if last_prob < 0.5:
        isSpam = False

    return isSpam




if __name__ == "__main__":
    msg = input("Enter grievance: ")
    spam = predict_spam(msg)
    print("spam was: ", spam)
    if not spam:
        department = predict_dept(msg)
        print("department was: ", department)
