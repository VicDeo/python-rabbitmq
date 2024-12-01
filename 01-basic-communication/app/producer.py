import os,pika

rabbit_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbit_queue = os.getenv('RABBITMQ_QUEUE', 'default_queue')

rabbit_user = os.getenv('RABBITMQ_USER', '')
rabbit_password = os.getenv('RABBITMQ_PASS', '')

try:
# Create connection
  params = pika.ConnectionParameters(host=rabbit_host,
                                     credentials=pika.credentials.PlainCredentials(rabbit_user, rabbit_password))
  connection = pika.BlockingConnection(params)

  # Create channel
  channel = connection.channel()

  # [Optional] Create Exchange and specify the bindings
  # We are working with default Exchange in this example 

  # Create queue if not exists already
  channel.queue_declare(queue=rabbit_queue)

  # Publish message
  channel.basic_publish(exchange="", routing_key=rabbit_queue, body="Alarm! I've been kidnapped!")

  print("Message has been sent")

  # Close the connection - closes channel as well
  connection.close()
except pika.exceptions.AMQPConnectionError:
  print("RabbitMQ is not running or env variables are incorrect")
