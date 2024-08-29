import json
import pika
from RabbitMQ.sender import send as send_message

SERVICE_ID = "A_UUiDv4"

def generate_transaction(id: str, description: str, amount: float):
    transaction = {
        "id": id,
        "description": description,
        "amount": amount,
        "tag": "A"
    }
    return transaction

def generate_request():
    transaction = generate_transaction("213", "description", 209.00)
    request = {
        "meta": {
            "id": SERVICE_ID,
            "type": "response",
            "source": "C",
            "subject": "transaction.record",
        },
        "data": [
            transaction
        ]
    }
    return request

def get_health_status(request_id:str):
    status = {
        "meta": {
            "id": SERVICE_ID,
            "type": "response",
            "source": "A",
            "subject": "health.A",
            "request_id": request_id
        },
        "data": 
        {
            "status": "ok"
        }
    }
    return json.dumps(status)



connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue="health.A")
channel.queue_declare(queue="generate.transaction")

def service_callback(ch, method, properties, body):
    print("Received Health check on A")
    send_message(name_of_queue="health.A_response", message=get_health_status("test"))

def make_request(ch, method, properties, body):
    print("Generated request details...")
    data = generate_request()
    print(data)
    send_message(name_of_queue="transaction.record", message=json.dumps(data))

channel.basic_consume(queue='health.A', auto_ack=True, on_message_callback=service_callback)
channel.basic_consume(queue='generate.transaction', auto_ack=True, on_message_callback=make_request)

print(' [*] Listening on A. To exit press CTRL+C')
channel.start_consuming()