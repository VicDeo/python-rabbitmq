# Broadcast / Fanout

* One to many communication
* Both producer and consumer create an exchange with the same name
* Routing is done by the exchange name, the route key is empty
* All existing consumers recieve the same message
* If there are no consumers when producer is working - message is discarded
* If queue is started as exclusive to a channel it can be used by this channel only, will get an unique name from RabbitMQ and will be destroyed with the respective channel on shutdown

`producer.py` produces 10 emergency messages
`consumer.py` consumes these messages, multiple instances can be started simultenously



P.S. Imho it's better to have `if_unused` as false, otherwise all existing consumers are detached after recieving the very first message as the exchange is removed by the producer. 

