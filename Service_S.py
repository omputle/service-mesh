import pika
import json
from RabbitMQ.sender import send as send_message

SERVICE_ID = "S_UUiDv4"

def store_transactions(request_data):
    transactions = request_data.get("data")
    f = open("transactions.txt", "a")
    for transaction in transactions:
        f.write(json.dumps(transaction))
        f.write("\n")
    f.close() 
    print("Transactions stored")

def retrieve_transactions():
    f = open("transactions.txt")
    raw_data = f.read()
    f.close()
    list_transactions = raw_data.split("\n")
    transactions = []
    for transaction in list_transactions:
        if transaction:
            transactions.append(json.loads(transaction))
    return transactions

def create_response(request_id):
    transactions = retrieve_transactions()
    response = {
        "meta": {
            "id": SERVICE_ID,
            "type": "response",
            "source": "S",
            "subject": "webhook.B",
            "request_id": request_id
        },
        "data": transactions
    }
    return response

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
channel.queue_declare(queue="transactions.statement")

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

def callback3(ch, method, properties, body):
    data = json.loads(body.decode("utf-8"))
    response = create_response(data["meta"]["id"])
    send_message(name_of_queue="transactions.statement_response", message=json.dumps(response))


channel.basic_consume(queue='transaction.record', auto_ack=True, on_message_callback=callback1)
channel.basic_consume(queue='transaction.tag', auto_ack=True, on_message_callback=callback2)
channel.basic_consume(queue='transactions.statement', auto_ack=True, on_message_callback=callback3)
channel.basic_consume(queue='health.S', auto_ack=True, on_message_callback=service_callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()