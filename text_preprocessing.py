# text_preprocessing.py
from flask import Flask, request
from traceback import format_exc
import pandas as pd
import re
import nltk
from nltk.tokenize import word_tokenize

app = Flask(__name__)

def remove_rt(text):
    if text.startswith("rt "):
        return text[3:]
    else:
        return text

def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove rt
    text = remove_rt(text)
    # Remove email
    text = re.sub(r'[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z0-9-.]+', ' ', text)
    # Remove url
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    # Remove domain
    text = re.sub(r'\.\w+\b', ' ', text)
    # Remove mention
    text = re.sub(r'@\w+', ' ', text)
    # Remove extra spacing
    text = re.sub(r'\s+', ' ', text)
    text_topic = text
    # Remove special chars
    text_topic = re.sub(r'[^a-z\s]', ' ', text_topic)
    # Remove two-char words
    text_topic = re.sub(r'\b\w{1,2}\b', ' ', text_topic)
    # Standardise famous ONG names
    text_topic = text_topic.replace("sea watch", "seawatch")
    text_topic = text_topic.replace("open arms", "openarms")
    text_topic = text_topic.replace("ocean viking", "oceanviking")
    text_topic = text_topic.replace("ocean vikings", "oceanviking")
    text_topic = text_topic.replace("oceanvikings", "oceanviking")
    text_topic = text_topic.replace("alarm phone", "alarmphone")
    text_topic = text_topic.replace("saving humans", "savinghumans")
    # Remove extra spacing
    text_topic = re.sub(r'\s+', ' ', text_topic)
    # Remove first and/or last blank space
    text = text.strip()
    text_topic = text_topic.strip()
    # Tokenize text
    words = word_tokenize(text_topic)
    # Remove digits
    words = [word for word in words if not word.isdigit()]
    # Remove stopwords
    stopwords_it = pd.read_csv("https://raw.githubusercontent.com/brema76/stopwords-ita/main/stopwords_it.csv")
    #stopwords_it = pd.read_csv("stopwords_it.csv")
    words = [word for word in words if not word in stopwords_it['word'].values]
    # Lemmatize text_topic
    lemmatization_it_fields = ['word','lemma']
    lemmatization_it = pd.read_csv("https://raw.githubusercontent.com/brema76/lemmatization-ita/master/lemmatization_ita.csv", names = lemmatization_it_fields)
    #lemmatization_it = pd.read_csv("lemmatization_ita.csv", names = lemmatization_it_fields)
    words = pd.DataFrame({'word': words})
    words = words.merge(lemmatization_it, on='word', how='left')
    words['word'] = words['lemma'].fillna(words['word'])
    words.drop(columns=['lemma'], inplace=True)
    words = words['word'].tolist()
    # Join words
    text_topic = ' '.join(words)
    return {"moral": text,
            "topic": text_topic}    

@app.route('/text_preprocessing', methods=['GET'])
def get_preprocessed_text():
    try:
        input_data = request.get_json()
        if "text" not in input_data:
            return {"error": "A field named 'text' in the JSON file is required"}, 400
        text = input_data["text"]
        text_preprocessing = preprocess_text(text)
        return {"text_preprocessing": text_preprocessing}, 200
    except Exception:
        return {"error": format_exc()}, 400

if __name__ == '__main__':
    app.run(debug=True)
