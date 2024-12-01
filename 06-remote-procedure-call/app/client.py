import os
import pika
import uuid

class FastRPCClent:
  def __init__(self, host, user, password, server_queue_name, client_queue_name):
    # Create connection
    params = pika.ConnectionParameters(host=rabbit_host,
                                     credentials=pika.credentials.PlainCredentials(rabbit_user, rabbit_password))
    self.connection = pika.BlockingConnection(params)
    self.channel = self.connection.channel()
    
    self.queue_name = client_queue_name
    self.server_queue_name = server_queue_name
    
    # Register the response queue
    self.channel.queue_declare(queue=self.queue_name, exclusive=True)
    
    self.channel.basic_consume(queue=self.queue_name,
                               on_message_callback=self.on_response,
                               auto_ack=True)
    
  def on_response(self, cn, method, props, body):
    if self.correlation_id == props.correlation_id:
      self.response = body

  def call(self, n):
    self.response = None
    self.correlation_id = str(uuid.uuid4())
    self.channel.basic_publish(exchange='',
                               routing_key=self.server_queue_name,
                               properties=pika.BasicProperties(
                                  reply_to=self.queue_name,
                                  correlation_id=self.correlation_id
                               ),
                               body=str(n)
                               )
                               
    while self.response is None:
      self.connection.process_data_events()
  
    return int(self.response)
  
rabbit_host = os.getenv('RABBITMQ_HOST', 'localhost')
rabbit_server_queue = os.getenv('RABBITMQ_SERVER_QUEUE', 'rpc_server_queue')
rabbit_client_queue = os.getenv('RABBITMQ_CLIENT_QUEUE', 'rpc_client_queue')

rabbit_user = os.getenv('RABBITMQ_USER', '')
rabbit_password = os.getenv('RABBITMQ_PASS', '')

try:
# Create connection
  rpc_client = FastRPCClent(rabbit_host, rabbit_user, rabbit_password, rabbit_server_queue, rabbit_client_queue)
  n=5
  f = rpc_client.call(n)
  print(f"{n}!={f}")
except pika.exceptions.AMQPConnectionError:
  print("RabbitMQ is not running or env variables are incorrect")
