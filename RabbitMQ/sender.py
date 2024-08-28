import pika

def send(message, name_of_queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=name_of_queue)
    channel.basic_publish(
        exchange='',
        routing_key=name_of_queue,
        body=message
    )
    connection.close()