# Basic communication case

* One to one communication
* Both producer and consumer create a queue with the same name
* Routing is done by the queue name
* Default Exchange is used - no need to create a new one
* Multiple consumers get messages in a Round Robin fashion
* Queue is not deleted on shutdown so if the producer send message before consumer is started - the message will be waiting in the queue until it is consumed

`producer.py` produces an emergency message
`consumer.py` consumes this message, multiple instances can be started simultaneously
