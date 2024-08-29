import json
import pika
from RabbitMQ.sender import send as send_message

SERVICE_ID = ""

def generate_transaction(id: str, description: str, amount: float, tag: str):
    transaction = {
        "id": id,
        "description": description,
        "amount": amount,
        "tag": tag
    }
    return json.dumps(transaction)

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

send_message(name_of_queue="transaction.record", message="from A")

# connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = connection.channel()

# channel.queue_declare(queue="transaction.new")

# def callback(ch, method, properties, body):
#     print("Received transaction from S")
#     send_message(name_of_queue="transaction.tag", message="sending back transaction")

# channel.basic_consume(queue='transaction.new', auto_ack=True, on_message_callback=callback)

# print(' [*] Waiting for messages. To exit press CTRL+C')
# channel.start_consuming()