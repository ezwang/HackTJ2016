#!/usr/bin/env python3

from flask import *

app = Flask(__name__, static_url_path='')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
