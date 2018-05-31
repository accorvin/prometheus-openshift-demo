#! /usr/bin/env python3

import logging
import sys

from flask import Flask

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
    return 'Hello, world!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
