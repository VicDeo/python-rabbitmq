import os
import pika
import random

rabbit_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbit_exchange = os.getenv('RABBITMQ_EXCHANGE', 'default_exchange')

rabbit_user = os.getenv('RABBITMQ_USER', '')
rabbit_password = os.getenv('RABBITMQ_PASS', '')


priorities = ["Low", "Medium", "High"]
categories = ["Alert", "Suggestion", "Complaint"]
places = ["Trafalgar square", "Empire State Building", "Niagara Falls"]

alerts = [
  "There is a fire at %s",
  "The quality of street lights should be improved at %s",
  "Complaint: High:  The electricity is not operational at %s"
]


def get_random_item(input_list):
  item_id = random.randint(0, len(input_list)-1)
  return input_list[item_id]

try:
# Create connection
  params = pika.ConnectionParameters(host=rabbit_host,
                                     credentials=pika.credentials.PlainCredentials(rabbit_user, rabbit_password))
  connection = pika.BlockingConnection(params)

  # Create channel
  channel = connection.channel()

  # Create an exchange of the topic type
  channel.exchange_declare(exchange=rabbit_exchange, exchange_type='topic')
  
  for i in range(10):
    # Publish message
    priority = get_random_item(priorities)
    category = get_random_item(categories)
    routing_key = f"{priority}.{category}"

    message = get_random_item(alerts) % get_random_item(places)
    message = f"{routing_key}::{message}"

    channel.basic_publish(exchange=rabbit_exchange, routing_key=routing_key, body=message)
    print(f"[x] sent {message}")

  # Cleanup
  try:
    channel.exchange_delete(exchange=rabbit_exchange, if_unused=True)
  except pika.exceptions.ChannelClosedByBroker:
    pass
  

  # Close the connection - closes channel as well
  connection.close()
except pika.exceptions.AMQPConnectionError:
  print("RabbitMQ is not running or env variables are incorrect")
