from flask import jsonify, request, Flask
from SentimentAnalysisLoadData import get_sentiment_prediction, load_model, load_tokenizer

app = Flask(__name__)

#Just to check the Flask setup.
@app.route('/')
def index():
    return jsonify('Welcome to Pi-Blog')

#This routing will accept comment through browser url (text/html)
@app.route('/sentiment/<comment>')
def sentiment_analysis_url(comment):
    commentString = comment #The input comment
    model = load_model() #invoke LSTM trained model
    tokenizer = load_tokenizer() #perform tokenization
    sentiment, score = get_sentiment_prediction(model, tokenizer, commentString) #predicting the sentiment of the comment along with score
    return jsonify(sentiment=sentiment)


#This routing will accept comment in JSON format and output will be generated in JSON format itself.
@app.route('/api/sentiment', methods=['POST'])
def sentiment_analysis_using_api():
    blogComment = request.get_json() #To accept POST request in JSON format
    comment = blogComment['comment'] # {"comment":"comment text"}
    model = load_model()
    tokenizer = load_tokenizer()
    sentiment, score = get_sentiment_prediction(model, tokenizer, comment)
    return jsonify(sentiment=sentiment)


if __name__ == "__main__":
    app.run()