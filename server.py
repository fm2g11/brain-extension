#!/usr/bin/env python3
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import util

UI_DIR = 'ui/'
DATA_FILE = 'data/items.json'
DATA = util.readjson(DATA_FILE)


def get_params(path):
    params_temp = parse_qs(urlparse(path).query)
    params = {}
    for param in params_temp:
        params[param] = params_temp[param][0]
    return params


def get_path(path):
    path = path.split('?')[0][1:]
    if path == '':
        path = 'index.html'
    return path


def add(key, val, tags):
    global DATA
    tags = (tag.strip() for tag in tags.lower().split(','))
    tags = sorted(set(t for t in tags if len(t)))
    matches = [item for item in DATA if item['key'] == key]
    if matches:
        matches[0]['val'] = val
        matches[0]['tags'] = tags
    else:
        DATA.append({
            'key': key,
            'val': val,
            'tags': tags,
        })
    DATA.sort(key=lambda x: x['key'])
    util.writejson(DATA, DATA_FILE)


def get():
    return json.dumps(DATA)


def exists(key):
    keys = (item['key'] for item in DATA)
    if key in keys:  # TODO: use binary search
        return json.dumps(True)
    return json.dumps(False)


def getitem(index):
    global DATA  # TODO: Package into class
    index = int(index)
    item = DATA[index]
    return json.dumps(item)


def delete(index):
    global DATA
    index = int(index)
    DATA = DATA[:index] + DATA[index+1:]
    util.writejson(DATA, DATA_FILE)


class RequestHandler(SimpleHTTPRequestHandler):

    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        path = ''
        params = get_params(self.path)
        response = bytes('{}', 'utf8')
        print(util.blue(str(params)))
        if 'add' in params and 'key' in params and 'val' in params:
            tags = params['tags'] if 'tags' in params else ''
            add(params['key'], params['val'], tags)
            self.send_header('Content-type', 'application/json')
        elif 'del' in params and 'index' in params:
            delete(params['index'])
            self.send_header('Content-type', 'application/json')
        elif 'get' in params:
            response = bytes(get(), 'utf8')
            self.send_header('Content-type', 'application/json')
        elif 'exists' in params and 'key' in params:
            response = bytes(exists(params['key']), 'utf8')
            self.send_header('Content-type', 'application/json')
        elif 'getitem' in params and 'index' in params:
            response = bytes(getitem(params['index']), 'utf8')
            self.send_header('Content-type', 'application/json')
        else:
            path = get_path(self.path)
            response = util.read(UI_DIR + path, bin=True)

        # Send headers
        self.send_header('Access-Control-Allow-Origin', '*')

        if path.endswith('.css'):
            self.send_header('Content-type', 'text/css')
        elif path.endswith('.js'):
            self.send_header('Content-type', 'text/javascript')
        elif path.endswith('.html'):
            self.send_header('Content-type', 'text/html')
        elif path.endswith('.jpg'):
            self.send_header('Content-type', 'image/jpeg')
        self.end_headers()
        self.wfile.write(response)
        return


def run():
  print('starting server...')
  # Server settings
  # Choose port 8080, for port 80, which is normally used for a http server,
  # you need root access
  # server_address = ('192.168.3.14', 8000)
  server_address = ('0.0.0.0', 8888)

  httpd = HTTPServer(server_address, RequestHandler)
  print('running server...')
  httpd.serve_forever()


run()
