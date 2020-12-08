import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import re

def load_tokenizer():

    """
    Returns tokenizer50k.pickle file of the tokenizer trained on amazon reviews

    Parameters:
        None


    Returns:
        tokenizer : pickle file containing the tokenizer
    """

    with open('SentimentAnalysisModelData/tokenizer50k.pickle', 'rb') as f:
        tokenizer = pickle.load(f)
    return tokenizer

def load_model():


    """
    Returns lstm_model.hdf5 file of the LSTM model trained on amazon reviews

    Parameters:
        None


    Returns:
        model : hdf5 file containing the trained model
    """

    model = tf.keras.models.load_model('SentimentAnalysisModelData/lstm_model.hdf5')
    return model

def normalize_texts(texts):

    """
    Returns the text removing punctuations, non ascii characters and non-binary digits

    Parameters:
        texts(list)            : list containing string elements


    Returns:
        normalized_texts(list) : list containing cleaned string elements
    """

    NON_ALPHANUM = re.compile(r'[\W]')
    NON_ASCII = re.compile(r'[^a-z0-1\s]')
    normalized_texts = []
    for text in texts:
        lower = text.lower()
        no_punctuation = NON_ALPHANUM.sub(r' ', lower)
        no_non_ascii = NON_ASCII.sub(r'', no_punctuation)
        normalized_texts.append(no_non_ascii)
    return normalized_texts

def get_sentiment_prediction(model, tokenizer, text):


    """
    Returns the sentiment of given text/s based on the polarity score of the sentiment.

    If the polarity score is greater than the threshold then sentence is classified as Positive
        otherwise Negative

    Threshold = 0.5

    Parameters:
        model                          : deep sequential model trained for sentiment analysis

        tokenizer                      : trained tokenizer

        text(string/list of strings)   : text/s of which the sentiment is to be predicted


    Returns:
        normalized_texts(list) : list containing cleaned string elements
    """

    text = [text]
    text = normalize_texts(text)
    max_length = 257
    trunc_type = 'post'
    text = tokenizer.texts_to_sequences(text)
    text = pad_sequences(text, maxlen=max_length)
    score = model.predict(text)[0][0]
    score = float("{:.3f}".format(score))
    sentiment = 'Positive' if score >= 0.5 else 'Negative'
    return sentiment, score
