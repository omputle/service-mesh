from flask import Flask
from flask import request
import json
import pika
from RabbitMQ.sender import send as send_message
from RabbitMQ.listener import listen_message

app = Flask(__name__)


SERVICE_ID = "G_UUiDv4"

@app.route("/", methods=['GET'])
def hello_world():
    send_message(message="From HTTP", name_of_queue="hello")
    return "<p>Hello World</p>"

@app.route("/S/statement")
def statement():
    transaction = {
        "meta": {
            "id": SERVICE_ID,
            "type": "request",
            "source": "G",
            "subject": "transactions.statement",
        },
        "data": "null"
    }
    send_message(message=json.dumps(transaction), name_of_queue='transactions.statement')
    response = listen_message(name_of_queue="transactions.statement_response")
    return response

@app.route("/webhook/B", methods=['POST'])
def webhook():
    transactions = request.data
    json_obj = {
        "meta": {
            "id": SERVICE_ID,
            "type": "request",
            "source": "G",
            "subject": "webhook.B",
        },
        "data": transactions.decode('utf-8')
    }
    send_message(message=json.dumps(json_obj), name_of_queue='webhook.B')
    return request.data

@app.route("/health/<service>")
def service_health(service):
    print("started")
    #service = request.base_url.split('/')[4]
    if service == 'G':
        json_obj = {
            "meta": {
                "id": SERVICE_ID,
                "type": "request",
                "source": "G",
                "subject": "health.G",
            },
            "data": {
                "status": "ok"
            }
        }
        return json.dumps(json_obj)
    else:
        send_message(name_of_queue='health.' + service, message="status")
        response = listen_message(name_of_queue='health.' + service + "_response")
        print(response)
        return response

