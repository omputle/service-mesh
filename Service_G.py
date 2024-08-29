import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue="webhook.B")

def callback(ch, method, properties, body):
    msg = json.loads(body)
    print(f" [X] Received From")
    print(msg)
            

channel.basic_consume(queue='webhook.B', auto_ack=True, on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()