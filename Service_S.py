import pika
import json
from RabbitMQ.sender import send as send_message

SERVICE_ID = ""

def store_transactions(request_data):
    transactions = request_data.get("data")
    f = open("transactions.txt", "a")
    for transaction in transactions:
        f.write(json.dumps(transaction))
        f.write("\n")
    f.close() 
    print("Transactions stored")


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
channel.queue_declare(queue="health.S")

def callback1(ch, method, properties, body):
    print(body)
    print(type(body))
    data = json.loads(body.decode("utf-8"))
    store_transactions(data)
    # send_message(name_of_queue="transaction.new", message=json.dumps(data))

def callback2(ch, method, properties, body): 
    print("Storing and sending to db")

def service_callback(ch, method, properties, body):
    print("Received Health check on S")
    send_message(name_of_queue="health.S_response", message=get_health_status("test"))


channel.basic_consume(queue='transaction.record', auto_ack=True, on_message_callback=callback1)
channel.basic_consume(queue='transaction.tag', auto_ack=True, on_message_callback=callback2)
channel.basic_consume(queue='health.S', auto_ack=True, on_message_callback=service_callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()