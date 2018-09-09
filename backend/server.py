#!/usr/bin/env python3
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import base64
from backend import util
from backend.brain import Brain
from backend.constants import UI_DIR, __prog__

brain = Brain()


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


class RequestHandler(SimpleHTTPRequestHandler):
    KEY = ''

    def do_HEAD(self):
        """ head method """
        print("send header")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_authhead(self):
        """ do authentication """
        print("send header")
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_auth(self):
        auth = self.headers.get_all('Authorization')
        if auth is None:
            self.do_authhead()
            self.wfile.write(b'no auth header received')
        elif auth[0] == 'Basic ' + self.KEY.decode('utf8'):
            return True
        else:
            self.do_authhead()
            self.wfile.write(auth[0].encode('utf8'))
            self.wfile.write(b'not authenticated')
        return False

    def do_GET(self):
        if not self.do_auth():
            return
        # Send response status code
        self.send_response(200)
        path = ''
        params = get_params(self.path)
        response = bytes('{}', 'utf8')
        print(util.blue(params.__repr__().encode('utf8')))
        if 'del' in params and 'index' in params:
            brain.delete(params['index'])
            self.send_header('Content-type', 'application/json')
        elif 'get' in params:
            response = bytes(brain.get(), 'utf8')
            self.send_header('Content-type', 'application/json')
        elif 'getitem' in params and 'index' in params:
            response = bytes(brain.getitem(params['index']), 'utf8')
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

    def do_POST(self):
        if not self.do_auth():
            return

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        data_string = data_string.decode("utf-8")
        data = get_params('?' + data_string)
        print(util.blue(data))

        response = bytes('{}', 'utf8')
        if 'add' in data and 'key' in data and 'val' in data:
            tags = data['tags'] if 'tags' in data else ''
            brain.add(data['key'], data['val'], tags)
        elif 'exists' in data and 'key' in data:
            response = bytes(brain.exists(data['key']), 'utf8')

        self.wfile.write(response)
        return


def run():
    print('starting server...')
    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server,
    # you need root access
    # server_address = ('192.168.3.14', 8000)

    parser = argparse.ArgumentParser(prog=__prog__)
    parser.add_argument('port', type=int, help='port number')
    parser.add_argument('key', help='username:password')
    args = parser.parse_args()
    RequestHandler.KEY = base64.b64encode(args.key.encode('utf8'))

    port = int(args.port)
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'running server on port: {port}')
    httpd.serve_forever()


run()
