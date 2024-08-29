import json
import pika
from RabbitMQ.sender import send as send_message

send_message(name_of_queue="generate.transaction", message="generate")