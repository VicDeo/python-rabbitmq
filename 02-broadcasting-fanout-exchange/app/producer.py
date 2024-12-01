import os,pika

rabbit_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbit_exchange = os.getenv('RABBITMQ_EXCHANGE', 'default_exchange')

rabbit_user = os.getenv('RABBITMQ_USER', '')
rabbit_password = os.getenv('RABBITMQ_PASS', '')

try:
# Create connection
  params = pika.ConnectionParameters(host=rabbit_host,
                                     credentials=pika.credentials.PlainCredentials(rabbit_user, rabbit_password))
  connection = pika.BlockingConnection(params)

  # Create channel
  channel = connection.channel()

  # Create an exchange
  channel.exchange_declare(exchange=rabbit_exchange, exchange_type='fanout')
  
  for i in range(4):
    # Publish message
    message = f"SOS! I've been kidnapped {i} hours ago!"
    channel.basic_publish(exchange=rabbit_exchange, routing_key='', body=message)
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
