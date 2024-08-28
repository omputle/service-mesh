from flask import Flask
from flask import request
import json
import pika
from RabbitMQ.sender import send as send_message

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello_world():
    send_message(message="From HTTP", name_of_queue="hello")
    return "<p>Hello World</p>"

@app.route("/S/statement")
def statement():
    json_obj = {
        "meta": {
            "id": "",
            "type": "request",
            "source": "G",
            "subject": "transactions.statement",
        },
        "data": "null"
    }
    send_message(message=json.dumps(json_obj), name_of_queue='hello')
    return "<p>Statement</p>"

@app.route("/webhook/B", methods=['POST'])
def webhook():
    send_message(message=request.data, name_of_queue="hello")
    return request.data

@app.route("/health/G")
def service_health():
    return "<p>OK!</p>"