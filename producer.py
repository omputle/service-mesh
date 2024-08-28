import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue="hello")
channel.basic_publish(exchange='', routing_key='hello', body=json.dumps({"name": "Luffy", "gender": "female"}, indent=4))
print(" [X] Sent 'Hello World!'")
connection.close()