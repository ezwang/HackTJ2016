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
TTSLock = th.Lock()

currentWords = {}

from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client['hacktj']

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


@app.route('/addWord')
def addWord():
    word = request.args.get('word')
    th.Thread(target=getTTSAsync, args=(word,)).run()
    return 'True'


@app.route('/delWord')
def delWord():
    word = request.args.get('word')
    th.Thread(target=delTTSAsync, args=(word,)).run()
    return 'True'


def delTTSAsync(word):
    TTSLock.acquire()
    try:
        del(currentWords[word])
    except ValueError:
        pass
    TTSLock.release()


def getTTSAsync(word):
    out = requests.get('https://api.voicerss.org/', params={'key': '970f71e61a4b4c8abd6af0d1f6a5326e', 'src': word, 'hl': 'zh-cn', 'r': -5})
    TTSLock.acquire()
    currentWords[word] = out
    TTSLock.release()


@app.route('/saveSet')
def saveWordList():
    name = request.args.get('label')
    words = request.args.get('words')
    db.lists.insert({'label':name, 'words':words})
    return 'True'


@app.route('/loadSet')
def loadWordList():
    name = request.args.get('label')
    try:
        data = db.lists.find({'label':name})
        return jsonify(**{'data': json.loads(data[0]['words'])})
    except IndexError:
        return jsonify(**{'data': []})

@app.route('/getListOfSets')
def getListList():
    return jsonify(**{'data': [x['label'] for x in db.lists.find()]})


@app.route('/deleteSet')
def deleteWordList():
    name = request.args.get('label')
    try:
        db.lists.delete_many({'label':name})
    except TypeError:
        return 'False'
    return 'True'


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
    try:
        TTSLock.acquire()
        out = Response(currentWords[phrase], mimetype='audio/mpeg')
        TTSLock.release()
        return out
    except KeyError:
        audio = requests.get('https://api.voicerss.org/', params={'key': '970f71e61a4b4c8abd6af0d1f6a5326e', 'src': phrase, 'hl': 'zh-cn', 'r': -5})
        return Response(audio.content, mimetype='audio/mpeg')


def saveWords():
    fileLock.acquire()
    with open('savedWords.json', 'w') as jsonFile:
        json.dump(savedWords, jsonFile)
    fileLock.release()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
