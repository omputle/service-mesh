from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello World</p>"

@app.route("/S/statement")
def statement():
    return "<p>Statement</p>"

@app.route("/webhook/B", methods=['POST'])
def webhook():
    print(request)
    return request

@app.route("/health/G")
def service_health():
    return "<p>OK!</p>"