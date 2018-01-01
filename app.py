import json
import os
import time

from flask import Flask, render_template, request

from analysis import filtering

app = Flask(__name__)

# On Bluemix, get the port number from the environment variable VCAP_APP_PORT
# When running this app on the local machine, default the port to 8080
PORT = int(os.getenv('VCAP_APP_PORT', 8080))
HOST = str(os.getenv('VCAP_APP_HOST', 'localhost'))


@app.route('/')
def index():
    flights = filtering.get_flights(start_date="")

    return render_template('index.html', flights=flights)


if __name__ == '__main__':
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    app.debug = True
    app.run(host=HOST, port=PORT)
