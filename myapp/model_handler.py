import re
from nltk.corpus import stopwords
import joblib
import pathlib
parent_dir = pathlib.Path(__file__).parent.resolve()


REPLACE_BY_SPACE_RE = re.compile('[/(){}\\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))


def clean_text(text):
    
    text = text.lower() # lowercase text
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # remove stopwors from text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text. substitute the matched string in REPLACE_BY_SPACE_RE with space.
    text = BAD_SYMBOLS_RE.sub('', text) # remove symbols which are in BAD_SYMBOLS_RE from text. substitute the matched string in BAD_SYMBOLS_RE with nothing. 
    text = text.replace('x', '')
    
    return text


# The maximum number of words to be used. (most frequent)
MAX_NB_WORDS = 100
# Max number of words in each complaint.
MAX_SEQUENCE_LENGTH = 20
# This is fixed.
EMBEDDING_DIM = 2



def predict_dept(message):
    return "1"



def predict_spam(message):

    message = clean_text(message)

    model = False
    model = joblib.load(parent_dir / 'spam_classifier_naive_bayes.joblib')
    vectorizer = joblib.load(parent_dir / 'tfidf_vectorizer.joblib')

    new_messages = [message]
    new_messages_tfidf = vectorizer.transform(new_messages)
    
    predictions = model.predict(new_messages_tfidf)

    return bool(predictions[0])




if __name__ == "__main__":
    msg = input("Enter grievance: ")
    spam = predict_spam(msg)
    print("spam was: ", spam)
    if not spam:
        department = predict_dept(msg)
        print("department was: ", department)
