import pika
import json
from RabbitMQ.sender import send as send_message

SERVICE_ID = ""

def get_health_status(request_id:str):
    status = {
        "meta": {
            "id": SERVICE_ID,
            "type": "response",
            "source": "C",
            "subject": "health.C",
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

channel.queue_declare(queue="transaction.new")

def callback(ch, method, properties, body):
    print("Received transaction from S")
    send_message(name_of_queue="transaction.tag", message="sending back transaction")

channel.basic_consume(queue='transaction.new', auto_ack=True, on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()