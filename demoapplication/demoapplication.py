#! /usr/bin/env python3

import logging
import sys

from flask import Flask, Response
from prometheus_client import generate_latest, Counter

requests_count = Counter('requests_count', 'The number of requests')

app = Flask(__name__)
log = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(('%(asctime)s - %(name)s - '
                               '%(levelname)s - %(message)s'))
log.setFormatter(formatter)
log.setLevel(logging.INFO)
app.logger.addHandler(log)
app.logger.setLevel(logging.INFO)


@app.route('/')
def hello():
    app.logger.info('Got a request')
    requests_count.inc()
    return 'Hello, world!'


@app.route('/metrics/')
def metrics():
    return Response(generate_latest())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
