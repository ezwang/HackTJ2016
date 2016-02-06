#!/usr/bin/env python3

from flask import *

app = Flask(__name__)


@app.route('/')
def index():
    return '<marquee>WordPolo</marquee>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=False)
