import pickle
import nltk
import string
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Load ML model
tfidf = pickle.load(open("vectorizer.pkl", "rb"))
model = pickle.load(open("model.pkl", "rb"))

ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    tokens = []
    for word in text:
        if word.isalnum():
            tokens.append(word)

    filtered = []
    for word in tokens:
        if word not in stopwords.words("english") and word not in string.punctuation:
            filtered.append(ps.stem(word))

    return " ".join(filtered)

def analyze_sms(input_sms):
    transformed = transform_text(input_sms)
    vector_input = tfidf.transform([transformed])
    prob = model.predict_proba(vector_input)[0][1]
    risk_score = int(prob * 100)

    reasons = []

    keywords = ["urgent", "free", "win", "lottery", "click",
                "bank", "verify", "offer", "claim"]

    for word in keywords:
        if word in input_sms.lower():
            reasons.append(f"Keyword detected: {word}")

    if re.search(r"http|www", input_sms.lower()):
        reasons.append("Contains suspicious link")

    if re.search(r"₹|\$|lakh|crore", input_sms.lower()):
        reasons.append("Financial bait pattern detected")

    return {
        "risk_score": min(risk_score, 100),
        "reasons": reasons
    }