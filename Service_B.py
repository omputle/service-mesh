import pika
import json
from RabbitMQ.sender import send as send_message

SERVICE_ID = "B_UUiDv4"
def handle_webhook(request_data):
    transactions = json.loads(request_data.get("data"))
    for transaction in transactions:
        transaction["tag"] = "B"
    request_data["meta"]["subject"] = "transactions.record"
    request_data["data"] = transactions
    return request_data


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
channel.queue_declare(queue="health.B")

def callback1(ch, method, properties, body):
    print("Received array")
    data = json.loads(body.decode("utf-8"))
    tagged_msg = handle_webhook(data)
    send_message(name_of_queue="transaction.record", message=json.dumps(tagged_msg))

def callback2(ch, method, properties, body):
    print("Received Health check on B")
    # print(body.decode("utf-8"))
    send_message(name_of_queue="health.B_response", message=get_health_status("test"))

channel.basic_consume(queue='webhook.B', auto_ack=True, on_message_callback=callback1)
channel.basic_consume(queue='health.B', auto_ack=True, on_message_callback=callback2)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()