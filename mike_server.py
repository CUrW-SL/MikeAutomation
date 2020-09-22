import os
import sys
from builtins import print
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
from datetime import datetime

from main import input_process, model_run, output_process


HOST_ADDRESS = '10.138.0.18'
HOST_PORT = 8080
config_path = r"E:\MIKE\ProductionRun\hourly_run\MikeAutomation\config.json"


class StoreHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('Handle GET request...')
        if self.path.startswith('/input-process'):
            print('StoreHandler|input-process')
            try:
                query_components = parse_qs(urlparse(self.path).query)
                print('StoreHandler|query_components : ', query_components)
                [run_date] = query_components['run_date']
                [run_time] = query_components['run_time']
                print('StoreHandler|input-process|run_date : ', run_date)
                print('StoreHandler|input-process|run_time : ', run_time)
                bucket_time = _get_bucket_time(run_date, run_time)
                input_process(config_path, bucket_time)
                response = {'response': 'success'}
            except Exception as ex:
                print('StoreHandler|input-process|Exception : ', str(ex))
                response = {'response': 'failed'}
            reply = json.dumps(response)
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(str.encode(reply))

        if self.path.startswith('/model-run'):
            print('StoreHandler|mike-run')
            try:
                query_components = parse_qs(urlparse(self.path).query)
                print('StoreHandler|query_components : ', query_components)
                [run_date] = query_components['run_date']
                [run_time] = query_components['run_time']
                print('StoreHandler|model-run|run_date : ', run_date)
                print('StoreHandler|model-run|run_time : ', run_time)
                bucket_time = _get_bucket_time(run_date, run_time)
                model_run(config_path, bucket_time)
                response = {'response': 'success'}
            except Exception as ex:
                print('StoreHandler|model-run|Exception : ', str(ex))
                response = {'response': 'failed'}
            reply = json.dumps(response)
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(str.encode(reply))

        if self.path.startswith('/output-process'):
            print('StoreHandler|output-process')
            try:
                query_components = parse_qs(urlparse(self.path).query)
                print('StoreHandler|query_components : ', query_components)
                [run_date] = query_components['run_date']
                [run_time] = query_components['run_time']
                print('StoreHandler|output-process|run_date : ', run_date)
                print('StoreHandler|output-process|run_time : ', run_time)
                bucket_time = _get_bucket_time(run_date, run_time)
                output_process(config_path, bucket_time)
                response = {'response': 'success'}
            except Exception as ex:
                print('StoreHandler|output-process|Exception : ', str(ex))
                response = {'response': 'failed'}
            reply = json.dumps(response)
            self.send_response(200)
            self.send_header('Content-type', 'text/json')
            self.end_headers()
            self.wfile.write(str.encode(reply))


def _get_bucket_time(run_date, run_time):
    print('_get_bucket_time|run_date : ', run_date)
    print('_get_bucket_time|run_time : ', run_time)
    run_datetime = datetime.strptime('{} {}'.format(run_date, run_time), '%Y-%m-%d %H:%M:%S')
    bucket_time = run_datetime.strftime('%Y-%m-%d_%H-00-00')
    print('_get_bucket_time|bucket_time : ', bucket_time)
    return bucket_time


if __name__ == '__main__':
    try:
        print('starting MIKE win server...')
        arguments = len(sys.argv) - 1
        if arguments > 0:
            host_address = sys.argv[1]
            host_port = int(sys.argv[2])
        else:
            host_address = HOST_ADDRESS
            host_port = HOST_PORT
        print('starting win server on host {} and port {} '.format(host_address, host_port))
        server_address = (host_address, host_port)
        httpd = HTTPServer(server_address, StoreHandler)
        print('win server running on host {} and port {} ...'.format(host_address, host_port))
        httpd.serve_forever()
    except Exception as e:
        print('Exception : ', str(e))

