import pika, sys, os

def main(host, user, password, rabbit_exchange):

  def callback(cn, method, properties, body):
    print("[x] received %r" %body)

  try:
    # Create a connection
    params = pika.ConnectionParameters(host=host,
                                      credentials=pika.credentials.PlainCredentials(user, password))
    connection = pika.BlockingConnection(params)

    # Create a channel
    channel = connection.channel()
    
    # Create a topic exchange
    channel.exchange_declare(exchange=rabbit_exchange, exchange_type='topic')
        
    # Create an exclusive queue with the name provided by RabbitMQ
    # So it will be unique, used by a single channel only
    # and automatically removed once connection is closed
    result = channel.queue_declare(queue='', exclusive=True)
    
    queue_name = result.method.queue
    print(f'Subscriber queue name {queue_name}')
        
    # Associate the callback function with the message queue and exchange
    channel.queue_bind(exchange=rabbit_exchange, queue=queue_name, routing_key="#")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print("[*] Waiting for the messages. Press Ctrl+C to exit")
    
    channel.start_consuming()
  except pika.exceptions.AMQPConnectionError:
      print("RabbitMQ is not running or env variables are incorrect")


if __name__  == '__main__':
  try:
    rabbit_host = os.getenv('RABBITMQ_HOST', 'localhost')
    rabbit_exchange = os.getenv('RABBITMQ_EXCHANGE', 'default_exchange')
    rabbit_user = os.getenv('RABBITMQ_USER', '')
    rabbit_password = os.getenv('RABBITMQ_PASS', '')

    main(rabbit_host, rabbit_user, rabbit_password, rabbit_exchange)
  except KeyboardInterrupt:
    print("\nConsumer has been shutdown")
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)
