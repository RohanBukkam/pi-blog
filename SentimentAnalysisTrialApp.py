import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import re
from flask import Flask
from flask import jsonify
from SentimentAnalysisLoadData import load_tokenizer, load_model, get_sentiment_prediction

app = Flask(__name__)
model = load_model()
tokenizer = load_tokenizer()


@app.route('/')
def index():
    return 'Welcome to Pi-Blog'

@app.route('/sentiment/<text>')
def wordsentiment(text):

    """
        Returns sentiment of given text
    """

    wordString = text
    sentiment, score = get_sentiment_prediction(model, tokenizer, wordString)
    return sentiment

if __name__ == "__main__":
    app.run(debug=True)
