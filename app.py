from flask import Flask, request
from interfaces.base import initialize

app = Flask(__name__)


initialize(app)


if __name__ == '__main__':
    print(app.url_map)
    app.run(host='0.0.0.0', port='80')
