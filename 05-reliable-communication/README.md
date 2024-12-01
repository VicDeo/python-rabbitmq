# Reliable communication

* Problem 1. Message can be lost between publisher and broker. Publisher can ask if the message was received by broker
* Problem 2. Channel or connection can be closed. Publisher can be notified if the connection or channel was closed
* Problem 3. Exchange can be lost on the RabbitMQ restart
* Problem 4. Messages can be lost on the queue restart
* Problem 5. Subscriber can go down before the message is handled
* Problem 6. On subscriber can be overloaded 

`producer.py` produces multiple messages sent to different routes depending on the message priority and category
`consumer.py` consumes any messages

