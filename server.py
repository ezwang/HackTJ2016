#!/usr/bin/env python2

from flask import *
import json
import threading as th
import requests

app = Flask(__name__, static_url_path='')
with open('Uni2Pinyin.json') as the_file:
    pinyin = json.load(the_file)

with open('savedWords.json') as savedWordsJSON:
    savedWords = json.load(savedWordsJSON)

fileLock = th.Lock()

currentWords = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uni2pinyin')
def getPinYin():
    spoken = request.args.get('spoken')
    actual = request.args.get('actual')
    if len(actual) != len(spoken):
        return 'False'
    for c in range(len(spoken)):
        spoken_unicode = hex(ord(spoken[c]))[2:].upper()
        actual_unicode = hex(ord(actual[c]))[2:].upper()
        if spoken_unicode not in pinyin or actual_unicode not in pinyin or not (set(pinyin[spoken_unicode]) & set(pinyin[actual_unicode])):
            return 'False'
    return 'True'


@app.route('/saveSet')
def saveWordList():
    name = request.args.get('label')
    words = request.args.get('words')
    savedWords[name] = json.loads(words)
    t = th.Thread(target=saveWords)
    t.run()
    return 'True'


@app.route('/loadSet')
def loadWordList():
    name = request.args.get('label')
    try:
        return jsonify(**{'data': savedWords[name]})
    except KeyError:
        return ''


@app.route('/getListOfSets')
def getListList():
    return jsonify(**{'data': list(savedWords.keys())})


@app.route('/deleteSet')
def deleteWordList():
    name = request.args.get('label')
    if name in savedWords:
        del savedWords[name]
        t = th.Thread(target=saveWords)
        t.run()
        return 'True'
    return 'False'


@app.route('/loadMeaningFromFile')
def loadMeaningList():
    words = open('file.txt').read().split('\t')  # get file from js
    char_meaning = {}
    k = 0
    while k < len(words):
        char_meaning[words[k]] = words[k + 2]
    return char_meaning


@app.route('/loadPinyinFromFile')
def loadPinyinList():
    words = open('file.txt').read().split('\t')  # get file from js
    char_pinyin = {}
    k = 0
    while k < len(words):
        char_pinyin[words[k]] = words[k + 1]
    return char_pinyin


@app.route('/getTTS')
def getTTS():
    phrase = request.args.get('chars')
    audio = requests.get('https://api.voicerss.org/', params={'key': '970f71e61a4b4c8abd6af0d1f6a5326e', 'src': phrase, 'hl': 'zh-cn'})
    print(audio.headers)
    return Response(audio.content, mimetype='audio/mpeg')


def saveWords():
    fileLock.acquire()
    with open('savedWords.json', 'w') as jsonFile:
        json.dump(savedWords, jsonFile)
    fileLock.release()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
