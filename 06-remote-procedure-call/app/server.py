import os
import pika
import random
import sys
import time

def fact(n):
  if n<=1:
    return 1
  return n*fact(n-1)


def main(host, user, password, rabbit_server_queue):

  def on_request(cn, method, properties, body):
    reply_queue_name = properties.reply_to
    correlation_id = properties.correlation_id
    n = int(body)
    print(f"called fact({n})")
    
    response = fact(n)
    
    cn.basic_publish(exchange='', routing_key=reply_queue_name,
                     properties=pika.BasicProperties(correlation_id=correlation_id),
                     body = str(response)
                     )
    
    cn.basic_ack(delivery_tag=method.delivery_tag)

  try:
    # Create a connection
    params = pika.ConnectionParameters(host=host,
                                      credentials=pika.credentials.PlainCredentials(user, password))
    connection = pika.BlockingConnection(params)

    # Create a channel
    channel = connection.channel()
    
    channel.queue_declare(queue=rabbit_server_queue, durable=True, exclusive=False)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=rabbit_server_queue, on_message_callback=on_request)
    print("[*] Awaiting RPC requests. Press Ctrl+C to exit")
    
    channel.start_consuming()
  except pika.exceptions.AMQPConnectionError:
      print("RabbitMQ is not running or env variables are incorrect")


if __name__  == '__main__':
  try:
    rabbit_host = os.getenv('RABBITMQ_HOST', 'localhost')
    rabbit_server_queue = os.getenv('RABBITMQ_SERVER_QUEUE', 'rpc_server_queue')
    rabbit_user = os.getenv('RABBITMQ_USER', '')
    rabbit_password = os.getenv('RABBITMQ_PASS', '')

    main(rabbit_host, rabbit_user, rabbit_password, rabbit_server_queue)
  except KeyboardInterrupt:
    print("\nConsumer has been shutdown")
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)
