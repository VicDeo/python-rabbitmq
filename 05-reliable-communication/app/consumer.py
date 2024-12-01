import os
import pika
import random
import sys
import time

def main(host, user, password, rabbit_exchange):

  def callback(cn, method, properties, body):
    print("[x] received %r" %body)
    #randomSleep = 5
    
    # Simulate that we are working hard
    randomSleep = random.randint(1, 7)
    print("Working for ", randomSleep, "seconds")
    while randomSleep > 0:
        print(".", end="")
        time.sleep(1)
        randomSleep -= 1

    # Solves Problem 5 - ack the message manually after the processing is done
    cn.basic_ack(delivery_tag=method.delivery_tag)


  try:
    # Create a connection
    params = pika.ConnectionParameters(host=host,
                                      credentials=pika.credentials.PlainCredentials(user, password))
    connection = pika.BlockingConnection(params)

    # Create a channel
    channel = connection.channel()
    
    # Solves problem 3 - both producer and consumer
    # Create an exchange as durable so it will survive RabbitMQ reboot
    channel.exchange_declare(exchange=rabbit_exchange, exchange_type='direct', durable=True)

    queue_name='test_queue'
    
    # Solves problem 4 - queue should not be exclusive
    result = channel.queue_declare(queue=queue_name, durable=True, exclusive=False)
    
    priorities = ["Low", "Medium", "High"]
    for priority in priorities:        
      # Associate the callback function with the message queue and exchange
      channel.queue_bind(exchange=rabbit_exchange, queue=queue_name, routing_key=priority)

    # Solves problem 5 - message not acknowledged automatically - No 'auto_ack' param
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    print("[*] Waiting for the messages. Press Ctrl+C to exit")
    
    # Solves problem 6 - one subscriber can receive not more than 1 message at time
    # It gets new message only after it confirms that the previous message has been processed 
    channel.basic_qos(prefetch_count=1)
    
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
