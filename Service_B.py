import pika
import json
from RabbitMQ.sender import send as send_message

SERVICE_ID = ""

def get_health_status(request_id:str):
    status = {
        "meta": {
            "id": SERVICE_ID,
            "type": "response",
            "source": "B",
            "subject": "health.B",
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

channel.queue_declare(queue="webhook.B")

def callback(ch, method, properties, body):
    print("Received array")
    send_message(name_of_queue="transaction.record", message="sending transaction")

channel.basic_consume(queue='webhook.B', auto_ack=True, on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()