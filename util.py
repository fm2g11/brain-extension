from json import JSONDecodeError
import requests
import json
import pickle
import csv
import time
import urllib
import operator
import os
import sys
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter


def get(url, sent=None, headers=None, json=True):
    # get params should be part of url
    if sent:
        url += urllib.parse.quote(sent)
    try:
        if headers:
            r = requests.get(url, headers=headers)
        else:
            r = requests.get(url)
    except Exception as e:
        print(red(e))
        print(pink(url), blue(sent))

    if json:
        try:
            return r.json()
        except JSONDecodeError as e:
            print(red(e))
            print(pink(url), blue(sent))
            return {"value":"error"}
    else:
        return r.text


def post(url, data, headers=None):
    HEADERS={'Content-Type': 'application/json'}
    if headers:
        HEADERS.update(headers)
    # data is dict
    # get params should be part of url
    r = requests.post(url, data=json.dumps(data), headers=HEADERS)
    return r.json()


def mem(obj):
    size = sys.getsizeof(obj)
    if size < 1024:
        return f'{size} B'
    if size < 1024 * 1024:
        return f'{round(size/1024)} KB'
    if size < 1024 * 1024 * 1024:
        return f'{round(size/(1024*1024))} MB'
    return f'{round(size/(1024*1024*1024))} GB'

#############################

def words():
    return set(readlines('/usr/share/dict/words'))

#############################
def read(filename, bin=False):
    if bin:
        f = open(filename, 'rb')
    else:
        f = open(filename, 'r')
    text = f.read()
    f.close()
    return text

def write(text, filename, bin=False):
    if bin:
        f = open(filename, 'wb')
    else:
        f = open(filename, 'w')

    f.write(text)
    f.close()

def writelines(lines, filename, bin=False):
    write('\n'.join(lines), filename, bin=bin)

def readlines(filename):
    f = open(filename, 'r')
    sents = [x[:-1] for x in f.readlines()]
    f.close()
    return sents

def readcsv(filename, delimiter=',', quotes='"'):
    data = []
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotes)
        for row in reader:
            data.append(row)
    return data

def writecsv(data, filename, delimiter=',', quotes='"'):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotes)
        for row in data:
            writer.writerow(row)

def readjson(filename):
    return json.load(open(filename))

def writejson(obj, filename):
    json.dump(obj, open(filename,'w'), indent=2)

#############################
def start():
    return time.time()

def lapsed(start, formatted=True, unit='s'):
    time_lapsed = round((time.time() - start), 4)
    if unit == 'ms':
        time_lapsed *= 1000
    if not formatted:
        return time_lapsed
    return str(time_lapsed) + unit

def percent(i, tot):
    return str(round(100.0*i/tot,2)) + '%'

#############################
def sortdict(dic, rev=False):
    return sorted(dic.items(), key=operator.itemgetter(1), reverse=rev)

#############################
def save(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load(filename, v=False):
    start = time.time()
    with open(filename, 'rb') as input:
        obj = pickle.load(input)
        if v:
            print(f'Loaded in {time.time() - start}s')
        return obj

#############################
def files(dir):
    return [f for f in os.listdir(dir) if f[0] != '.']


def nlp():
    import spacy
    return spacy.load('en')

#############################
def red(s):
    return '\033[91m' + str(s) + '\033[0m'

def yellow(s):
    return '\033[93m' + str(s) + '\033[0m'

def green(s):
    return '\033[92m' + str(s) + '\033[0m'

def blue(s):
    return '\033[94m' + str(s) + '\033[0m'

def pink(s):
    return '\033[95m' + str(s) + '\033[0m'

def lightblue(s):
    return '\033[96m' + str(s) + '\033[0m'

def white(s):
    return '\033[97m' + str(s) + '\033[0m'

def underline(s):
    return '\033[4m' + str(s) + '\033[0m'

def bold(s):
    return '\033[1m' + str(s) + '\033[0m'

def light(s):
    return '\033[2m' + str(s) + '\033[0m'

def flash(s):
    return '\033[5m' + str(s) + '\033[0m'

def orangefill(s):
    return '\033[100m' + str(s) + '\033[0m'

def redfill(s):
    return '\033[101m' + str(s) + '\033[0m'


def greenfill(s):
    return '\033[102m' + str(s) + '\033[0m'


def yellowfill(s):
    return '\033[103m' + str(s) + '\033[0m'


def bluefill(s):
    return '\033[104m' + str(s) + '\033[0m'


def pinkfill(s):
    return '\033[105m' + str(s) + '\033[0m'


def lightbluefill(s):
    return '\033[106m' + str(s) + '\033[0m'


def whitefill(s):
    return '\033[107m' + str(s) + '\033[0m'


jl = JsonLexer()
tf = TerminalFormatter()


def pprint(obj):
    json_str = json.dumps(obj, indent=2, sort_keys=True)
    print(highlight(json_str, jl, tf))
