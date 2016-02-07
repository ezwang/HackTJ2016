# generates json file with unicode code to pinyin from Uni2Pinyin

import json

with open('Uni2Pinyin', 'r') as infile:
    with open('Uni2Pinyin.json', 'w') as outfile:
        json.dump({line.split()[0]: line.split()[1:] for line in infile.read().split('\n') if len(line.split())>1}, outfile)
