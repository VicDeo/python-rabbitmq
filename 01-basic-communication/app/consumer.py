import pika, sys, os

def main(host, user, password, queue_name):
  def callback(cn, method, properties, body):
    print("[x] received %r" %body)

  try:
    # Create a connection
    params = pika.ConnectionParameters(host=host,
                                      credentials=pika.credentials.PlainCredentials(user, password))
    connection = pika.BlockingConnection(params)

    # Create a channel
    channel = connection.channel()
    
    # Create a queue if not exists
    channel.queue_declare(queue_name)
    
    # Associate the callback function with the message queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print("[*] Waiting for the messages. Press Ctrl+C to exit")
    channel.start_consuming()
  except pika.exceptions.AMQPConnectionError:
      print("RabbitMQ is not running or env variables are incorrect")


if __name__  == '__main__':
  try:
    rabbit_host = os.getenv('RABBITMQ_HOST', 'localhost')
    rabbit_queue = os.getenv('RABBITMQ_QUEUE', 'default_queue')
    rabbit_user = os.getenv('RABBITMQ_USER', '')
    rabbit_password = os.getenv('RABBITMQ_PASS', '')

    main(rabbit_host, rabbit_user, rabbit_password, rabbit_queue)
  except KeyboardInterrupt:
    print("\nConsumer has been shutdown")
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)
