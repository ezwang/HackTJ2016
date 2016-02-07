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
    spoken = request.args.get('spoken')
    actual = request.args.get('actual')
    if len(actual) != len(spoken): return 'False'
    for c in range(len(spoken)):
        spoken_unicode = ord(spoken[c])
        actual_unicode = ord(actual[c])
        if spoken_unicode not in pinyin or actual_unicode not in pinyin or not (pinyin[spoken_unicode] & pinyin[actual_unicode]):
            return 'False'
    return 'True'


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
