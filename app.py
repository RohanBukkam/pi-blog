from utils import app

if __name__ == "__main__":
    app.debug = True
    # os.environ['PYTHONPATH'] = os.getcwd()
    app.run(host='127.0.0.1', port=5000)  # , use_reloader=False) , debug=False
