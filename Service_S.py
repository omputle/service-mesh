import pika
import json
from RabbitMQ.sender import send as send_message

SERVICE_ID = ""
def get_health_status(request_id:str):
    status = {
        "meta": {
            "id": SERVICE_ID,
            "type": "response",
            "source": "S",
            "subject": "health.S",
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

channel.queue_declare(queue="transaction.record")
channel.queue_declare(queue="transaction.tag")

def callback1(ch, method, properties, body):
    print("Received transaction From B")
    send_message(name_of_queue="transaction.new", message="sending transaction")

def callback2(ch, method, properties, body):
    print("Received transaction from C")
    print("Storing and sending to db")

channel.basic_consume(queue='transaction.record', auto_ack=True, on_message_callback=callback1)
channel.basic_consume(queue='transaction.tag', auto_ack=True, on_message_callback=callback2)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()