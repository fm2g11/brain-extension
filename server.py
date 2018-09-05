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


def add(key, val):
    DATA[key] = val
    util.writejson(DATA, DATA_FILE)


def get():
    return json.dumps(sorted(DATA.items()))


def exists(key):
    if key in DATA:
        return json.dumps(True)
    return json.dumps(False)


def getpair(index):
    index = int(index)
    data = sorted(DATA.items())
    return json.dumps({
        'key': data[index][0],
        'val': data[index][1]
    })


def delete(index):
    index = int(index)
    data = sorted(DATA.items())
    key = data[index][0]
    del DATA[key]
    util.writejson(DATA, DATA_FILE)


class RequestHandler(SimpleHTTPRequestHandler):

    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        path = ''
        params = get_params(self.path)
        response = '{}'
        print(util.blue(str(params)))
        if 'add' in params and 'key' in params and 'val' in params:
            add(params['key'], params['val'])
            self.send_header('Content-type', 'application/json')
        elif 'del' in params and 'index' in params:
            delete(params['index'])
            self.send_header('Content-type', 'application/json')
        elif 'get' in params:
            response = get()
            self.send_header('Content-type', 'application/json')
        elif 'exists' in params and 'key' in params:
            response = exists(params['key'])
            self.send_header('Content-type', 'application/json')
        elif 'getpair' in params and 'index' in params:
            response = getpair(params['index'])
            self.send_header('Content-type', 'application/json')
        else:
            path = get_path(self.path)
            response = util.read(UI_DIR + path)

        # Send headers
        self.send_header('Access-Control-Allow-Origin', '*')

        if path.endswith('.css'):
            self.send_header('Content-type', 'text/css')
        elif path.endswith('.js'):
            self.send_header('Content-type', 'text/javascript')
        elif path.endswith('.html'):
            self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes(response, 'utf8'))
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
