#!/usr/bin/env python2

from flask import *
import json

app = Flask(__name__, static_url_path='')
with open('Uni2Pinyin.json') as the_file:
    pinyin = json.load(the_file)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uni2pinyin')
def getPinYin():
    s = ord(request.args.get('spoken'))
    a = ord(request.args.get('actual'))
    return len(set(pinyin[s]) & set(pinyin[a])) > 0


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)