#!/usr/bin/env python3

import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import util

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

  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)
        path = None
        params = get_params(self.path)
        print(util.blue(str(params)))
        # if 'sentence' in params:
        #     response = ''
        #     response = bytes(json.dumps(response), 'utf-8')
        #     self.send_header('Content-type', 'application/json')
        # else:
        path = get_path(self.path)
        response = util.read(path, bin=True)
        # Send headers
        self.send_header('Access-Control-Allow-Origin', '*')

        if path and path.endswith('.css'):
            self.send_header('Content-type', 'text/css')
        elif path and path.endswith('.js'):
            self.send_header('Content-type', 'text/javascript')
        elif path and path.endswith('.html'):
            self.send_header('Content-type', 'text/html')
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
