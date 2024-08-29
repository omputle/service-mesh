import json
import pika

def listen_message(name_of_queue, sender=""):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # message = ""
    # def callback(ch, method, properties, body):
    #     print(f" [x] received on {sender}")
    #     return json.loads(body)
    
    for method_frame, propeties, body in channel.consume(name_of_queue):
        message = body.decode("utf-8")

        channel.basic_ack(method_frame.delivery_tag)
        if method_frame.delivery_tag == 1:
            break

        channel.close()
        connection.close()
        print(message)
    return message
