import os
import pika
import random

rabbit_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbit_exchange = os.getenv('RABBITMQ_EXCHANGE', 'default_exchange')

rabbit_user = os.getenv('RABBITMQ_USER', '')
rabbit_password = os.getenv('RABBITMQ_PASS', '')

def get_adj(exclude=''):
  adjs = ["an arthropod", "a roasted", "a waterfowl", "a shaved", "a stoned", "a disguised"]
  while True:
    adj_id = random.randint(0, len(adjs)-1)
    if adjs[adj_id] != exclude:
      break
  return adjs[adj_id]

try:
# Create connection
  params = pika.ConnectionParameters(host=rabbit_host,
                                     credentials=pika.credentials.PlainCredentials(rabbit_user, rabbit_password))
  connection = pika.BlockingConnection(params)

  # Create channel
  channel = connection.channel()

  # Create an exchange
  channel.exchange_declare(exchange=rabbit_exchange, exchange_type='direct')
  
  animals = ["Baboon", "Badger", "Donkey", "Guinea Pig", "Racoon"]
  for i in range(10):
    # Publish message
    animal_id = random.randint(0, len(animals)-1)
    animal = animals[animal_id]
    adj = get_adj()
    adj2 = get_adj(adj).split(' ')[1]
    
    message = f"SOS! I've been kidnapped by {adj} {adj2} {animal}!"
    channel.basic_publish(exchange=rabbit_exchange, routing_key=animal, body=message)
    print(f"[x] sent {message}")

  # Cleanup
  try:
    channel.exchange_delete(exchange=rabbit_exchange, if_unused=False)
  except pika.exceptions.ChannelClosedByBroker:
    pass
  

  # Close the connection - closes channel as well
  connection.close()
except pika.exceptions.AMQPConnectionError:
  print("RabbitMQ is not running or env variables are incorrect")
