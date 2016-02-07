#!/usr/bin/env python2

from flask import *
import json
import threading as th

app = Flask(__name__, static_url_path='')
with open('Uni2Pinyin.json') as the_file:
    pinyin = json.load(the_file)

with open('savedWords.json') as savedWordsJSON:
    savedWords = json.load(savedWordsJSON)

fileLock = th.Lock()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uni2pinyin')
def getPinYin():
    spoken = request.args.get('spoken')
    actual = request.args.get('actual')
    if len(actual) != len(spoken): return 'False'
    for c in range(len(spoken)):
        spoken_unicode = hex(ord(spoken[c]))[2:].upper()
        actual_unicode = hex(ord(actual[c]))[2:].upper()
        if spoken_unicode not in pinyin or actual_unicode not in pinyin or not (set(pinyin[spoken_unicode]) & set(pinyin[actual_unicode])):
            return 'False'
    return 'True'


@app.route('/saveList')
def saveWordList():
    name = request.args.get('label')
    l = request.args.get('words')
    savedWords[name] = json.loads(l)
    t = th.Thread(target=saveWords)
    t.run()
    return 'success'


@app.route('/getList')
def getWordList():
    name = request.args.get('label')
    try:
        return json.dumps(savedWords[name])
    except KeyError:
        return None


@app.route('/getListOfLists')
def getListList():
    return json.dumps(savedWords.keys)


def saveWords():
    fileLock.acquire()
    with open('savedWords.json', 'w') as jsonFile:
        json.dump(savedWords, jsonFile)
    fileLock.release()


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
