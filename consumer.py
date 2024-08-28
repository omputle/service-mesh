import pika
import sys
import os
import ast
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue="hello")

def callback(ch, method, properties, body):
    msg = json.loads(body)
    print(f" [X] Received")
    print(msg)
    
    # if msg['gender'] == 'male':
    #     print("it's a dude!!")
    # elif msg['gender'] == 'female':
    #     print("'ts a chick!")
    # else:
    #     print("no gender ")

channel.basic_consume(queue='hello', auto_ack=True, on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)