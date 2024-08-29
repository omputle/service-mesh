from flask import Flask
from flask import request
import json
import pika
from RabbitMQ.sender import send as send_message

app = Flask(__name__)


SERVICE_ID = ""

@app.route("/", methods=['GET'])
def hello_world():
    send_message(message="From HTTP", name_of_queue="hello")
    return "<p>Hello World</p>"

@app.route("/S/statement")
def statement():
    transaction = {
        "meta": {
            "id": "",
            "type": "request",
            "source": "G",
            "subject": "transactions.statement",
        },
        "data": "null"
    }
    send_message(message=json.dumps(transaction), name_of_queue='hello')
    return "<p>Statement</p>"

@app.route("/webhook/B", methods=['POST'])
def webhook():
    transactions = request.data
    json_obj = {
        "meta": {
            "id": "",
            "type": "request",
            "source": "G",
            "subject": "webhook.B",
        },
        "data": transactions.decode('utf-8')
    }
    send_message(message=json.dumps(json_obj), name_of_queue='webhook.B')
    return request.data

@app.route("/health/G")
def service_health():
    json_obj = {
        "meta": {
            "id": "",
            "type": "request",
            "source": "G",
            "subject": "health.G",
            "request_id": ""
        },
        "data": 
        {
            "status": "ok"
        }
    }
    return json_obj